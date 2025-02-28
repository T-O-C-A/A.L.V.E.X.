# AI Assistent met Zelflerende Functies

Dit project is een zelflerende AI-assistent die draait op Docker-containers en toegankelijk is via een webinterface. De AI kan:

✅ Google en Apple Agenda integreren 🗓️  
✅ Zelflerend gedrag vertonen en functies genereren 🤖  
✅ Code uitvoeren in een sandboxed Docker-container 🚀  
✅ Beschikbaar zijn via een webinterface (React) 🌐  
✅ Veilig en schaalbaar draaien met NGINX en SSL 🔐  

## 📂 Projectstructuur
```
AI-Assistent/
│── backend/
│   │── main.py
│   │── Dockerfile
│   │── requirements.txt
│   └── config.json
│
│── frontend/
│   │── src/
│   │   ├── components/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── styles.css
│   │── public/
│   │── package.json
│   │── Dockerfile
│
│── database/
│   │── init.sql
│   └── Dockerfile
│
│── nginx/
│   │── nginx.conf
│
│── docker-compose.yml
│── README.md
│── .gitignore
```

## 🚀 Installatie & Setup
### 1. **Clone deze repository**
```bash
git clone https://github.com/jouwgithub/AI-Assistent.git
cd AI-Assistent
```

### 2. **Omgevingsvariabelen instellen**
Maak een `.env` bestand en voeg je API-sleutels toe:
```
OPENAI_API_KEY=JOUW_OPENAI_API_KEY
APPLE_USERNAME=JOUW_ICLOUD_EMAIL
APPLE_PASSWORD=JOUW_APP_SPECIFIEK_WACHTWOORD
DATABASE_URL=postgres://user:password@db:5432/ai_db
```

### 3. **Start de containers met Docker Compose**
```bash
docker-compose up --build -d
```

De AI zal beschikbaar zijn op:
- **Frontend**: http://localhost:3000  
- **API Backend**: http://localhost:8000  
- **HTTPS Domeinnaam**: https://ai.mijndomein.com (indien ingesteld)  

## 🔧 Hoe Werkt de AI?
1. **Vraag stellen** → De AI verwerkt agenda-data & GPT-antwoorden.
2. **Nieuwe functies genereren** → AI genereert en test code in Docker-sandbox.
3. **Automatisch leren** → De AI detecteert patronen en stelt optimalisaties voor.

## 🌍 Domeinnaam & SSL Instellen
1. **Registreer een domeinnaam** (bijv. via Namecheap).
2. **Update je DNS-records** naar je server IP.
3. **Installeer SSL met Let's Encrypt**:
```bash
sudo certbot --nginx -d ai.mijndomein.com
```

## 🛠️ Extra Functionaliteiten
✅ **Spraakherkenning** (via Whisper STT)  
✅ **Integratie met Domotica (Home Assistant, MQTT)**  
✅ **Automatische routineherkenning & notificaties**  

## 🤝 Contributies
Pull requests zijn welkom! 🚀  

**Auteur:** [Jouw Naam] - 2025
