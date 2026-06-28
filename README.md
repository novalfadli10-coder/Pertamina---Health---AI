# Pertamina Health AI

## Deploy backend

### Render
1. Push repository ke GitHub.
2. Buka Render dan pilih New + > Web Service.
3. Hubungkan repo ini.
4. Pilih folder backend sebagai root directory.
5. Gunakan build command:
   ```bash
   pip install -r requirements.txt
   ```
6. Gunakan start command:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port $PORT
   ```
7. Set environment variables:
   - OPENROUTER_API_KEY
   - OPENROUTER_MODEL=openai/gpt-oss-120b
   - CORS_ORIGINS=https://your-frontend-domain.vercel.app

### Railway
1. Buat project baru.
2. Tambahkan service dari folder backend.
3. Set start command:
   ```bash
   uvicorn api:app --host 0.0.0.0 --port $PORT
   ```

## Deploy frontend

### Vercel
1. Push repository ke GitHub.
2. Buka Vercel dan pilih New Project.
3. Pilih folder frontend sebagai root directory.
4. Build command:
   ```bash
   npm run build
   ```
5. Output directory:
   ```bash
   dist
   ```
6. Set environment variable:
   - VITE_API_URL=https://your-backend-url.example.com
