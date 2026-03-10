<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Kwetu Agence</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { font-family: Arial, sans-serif; margin:0; padding:20px; background:#f0f2f5; }
h1 { text-align:center; }
button, input { width:100%; padding:12px; margin:8px 0; border-radius:6px; border:1px solid #ccc; }
button { background:#0a6efd; color:white; border:none; }
.container { max-width:400px; margin:auto; background:white; padding:20px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.2); }
</style>
</head>
<body>
<h1>Kwetu Agence 🚚</h1>
<div class="container">
  <h2>Connexion</h2>
  <input type="email" id="email" placeholder="Email">
  <input type="password" id="password" placeholder="Mot de passe">
  <button onclick="login()">Connexion</button>
  <hr>
  <h2>Envoyer un colis</h2>
  <input type="text" id="receiver" placeholder="Destinataire">
  <input type="text" id="fromCity" placeholder="Ville départ">
  <input type="text" id="toCity" placeholder="Ville arrivée">
  <input type="text" id="packageName" placeholder="Nom du colis">
  <button onclick="sendPackage()">Envoyer</button>
  <hr>
  <button onclick="exportCSV()">Exporter CSV</button>
</div>

<script>
let token = null;

async function login(){
  const email=document.getElementById("email").value;
  const password=document.getElementById("password").value;
  const res=await fetch("/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email,password})});
  const data=await res.json();
  if(data.token){ token=data.token; alert("Connexion réussie"); } else { alert("Erreur: "+data.error); }
}

async function sendPackage(){
  if(!token){ alert("Veuillez vous connecter"); return; }
  const receiver=document.getElementById("receiver").value;
  const fromCity=document.getElementById("fromCity").value;
  const toCity=document.getElementById("toCity").value;
  const packageName=document.getElementById("packageName").value;
  const res=await fetch("/packages",{method:"POST",headers:{"Content-Type":"application/json","Authorization":token},body:JSON.stringify({receiverName:receiver,fromCity,toCity,packageName,agencyId:1})});
  const data=await res.json();
  alert(data.message+" | Tracking: "+data.trackingNumber);
}

function exportCSV(){
  if(!token){ alert("Veuillez vous connecter"); return; }
  window.location="/packages/export";
}
</script>
</body>
</html>