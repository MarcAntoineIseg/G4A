# MCP GA4 Tool Server

Ceci est un serveur **Model Context Protocol (MCP)** qui s'intègre avec **Google Analytics 4 (GA4)** et prend en charge la communication avec les **agents n8n** via des webhooks et outils. Il permet aux agents IA d’accéder en toute sécurité aux données analytiques spécifiques à l’utilisateur à l’aide de tokens authentifiés liés à Supabase.

## Key Features

- Serveur API basé sur FastAPI avec routage modulaire
- Récupération des tokens OAuth depuis Supabase (par utilisateur)
- Intégration de l’API Google Analytics 4
- Format de réponse structuré compatible avec les outils d’agents OpenAI/n8n
- Route de manifeste MCP pour la découverte automatique par les LLMs
- Prêt pour le déploiement sur Railway ou d'autres plateformes cloud

## Project Structure

.  
├── app/  
│ ├── main.py # Point d'entrée FastAPI  
│ ├── routes/  
│ │ ├── ga4.py # Routeur pour les endpoints GA4  
│ │ └── tools.py # Manifeste d’outil MCP  
│ ├── services/  
│ │ ├── ga4_client.py # Logique de requête GA4  
│ │ └── supabase_client.py # Gestionnaire Supabase  
│ └── utils/  
│ └── token_handler.py # Rafraîchissement des tokens OAuth  
├── .env.example # Exemple de configuration pour déploiement  
├── requirements.txt  
├── Procfile # Fichier de déploiement Railway  


## MCP Endpoints

### `POST /ga4/get-sessions`

Retourne le nombre de sessions des 30 derniers jours pour l’utilisateur authentifié.  


#### Request Body
```json
{
  "userId": "user id",
  "googleAnalyticsData": {
    "selectedProperty": {
      "id": "123456778"
    }
  }
}
````

#### Response

```
{
  "message": "Session count retrieved",
  "data": {
    "metric": "sessions_last_30_days",
    "value": ""
  }
}
```

### `GET /mcp/tools`

Retourne le manifeste d’outils MCP au format compatible OpenAI.

## Environment Variables

Créez un fichier `.env` basé sur l’exemple fourni `.env.example` :

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-service-role-key
GA_SCOPES=https://www.googleapis.com/auth/analytics.readonly
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_API_ENDPOINT=https://analyticsdata.googleapis.com/v1beta
```

Ces clés sont utilisées pour récupérer en toute sécurité les tokens et les informations de connexion GA4 liées à chaque utilisateur.

## Deployment (Recommended: Railway)

Poussez votre code sur GitHub.

Connectez le dépôt à Railway.

Ajoutez vos variables `.env` dans l’onglet "Environment" de Railway.

Assurez-vous que le fichier `Procfile` existe avec le contenu suivant :

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Notes

Ce serveur suppose que les identifiants OAuth de l'utilisateur (tokens d’accès/rafraîchissement GA4, ID de propriété, info de compte) sont déjà stockés de manière sécurisée dans Supabase et liés par `user_id`.

Seule la métrique `get-sessions` est implémentée pour les tests initiaux.

Des métriques GA4 et outils supplémentaires (ex. `get-top-pages, get-top-countries, get-retention-data`) peuvent être ajoutés de manière modulaire.

Ce serveur est conçu pour s'intégrer à **Eliott** et permet un accès dynamique et sécurisé aux données via des agents LLM.


