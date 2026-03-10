import express from "express";
import cors from "cors";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

let users = [];
let packages = [];
let messages = [];

// Middleware JWT
function auth(req, res, next) {
  const token = req.headers["authorization"];
  if (!token) return res.status(403).json({ error: "Token manquant" });
  try {
    req.user = jwt.verify(token, "SECRET_KEY");
    next();
  } catch {
    res.status(401).json({ error: "Token invalide" });
  }
}

// Auth
app.post("/auth/register", async (req, res) => {
  const { name, email, password, type } = req.body;
  const hash = await bcrypt.hash(password, 10);
  const user = { id: Date.now(), name, email, passwordHash: hash, type };
  users.push(user);
  res.json({ message: "Utilisateur enregistré" });
});

app.post("/auth/login", async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user) return res.status(400).json({ error: "Utilisateur introuvable" });
  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) return res.status(401).json({ error: "Mot de passe incorrect" });
  const token = jwt.sign({ id: user.id, type: user.type }, "SECRET_KEY");
  res.json({ token, type: user.type });
});

// Colis
app.post("/packages", auth, (req, res) => {
  const { receiverName, fromCity, toCity, packageName, agencyId } = req.body;
  const trackingNumber = "KWETU-" + Date.now();
  const pkg = { senderId: req.user.id, receiverName, fromCity, toCity, packageName, agencyId, trackingNumber, status: "En cours" };
  packages.push(pkg);
  res.json({ message: "Colis créé", trackingNumber });
});

app.get("/packages/:trackingNumber", auth, (req, res) => {
  const pkg = packages.find(p => p.trackingNumber === req.params.trackingNumber);
  res.json(pkg || {});
});

// Export CSV
app.get("/packages/export", auth, (req, res) => {
  let csv = "Tracking,Receiver,From,To,Package,Status\n";
  packages.forEach(p => {
    csv += `${p.trackingNumber},${p.receiverName},${p.fromCity},${p.toCity},${p.packageName},${p.status}\n`;
  });
  res.header("Content-Type", "text/csv");
  res.attachment("packages.csv");
  res.send(csv);
});

// Messages
app.post("/messages", auth, (req, res) => {
  const { receiverId, agencyId, text } = req.body;
  const msg = { id: Date.now(), senderId: req.user.id, receiverId, agencyId, text };
  messages.push(msg);
  res.json({ message: "Message envoyé" });
});

app.get("/messages/:userId", auth, (req, res) => {
  const conv = messages.filter(m => m.receiverId == req.params.userId || m.senderId == req.params.userId);
  res.json(conv);
});

app.listen(4000, () => console.log("Kwetu Agence running on http://localhost:4000"));