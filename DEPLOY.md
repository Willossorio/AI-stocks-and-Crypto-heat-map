# Deploy for free on Render

This version is ready for Render’s free tier (sleeps when idle, wakes on first visit).

## Steps

1. Create a free GitHub account if you don’t have one.
2. Create a new public repository (e.g. `stock-heatmap`).
3. Upload the contents of this folder to the repo (app.py, templates/, requirements.txt, Procfile, README.md).
4. Go to [render.com](https://render.com) and sign up (free, GitHub login works).
5. Click **New → Web Service**.
6. Connect your GitHub repo.
7. Settings:
   - **Name**: anything you like
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
   - **Instance Type**: Free
8. Click **Create Web Service**.

After a few minutes you’ll get a URL like `https://your-app-name.onrender.com`.

### Notes
- Free services sleep after ~15 minutes of no traffic. The first load in the morning takes 30–60 seconds while it wakes up — normal.
- No credit card required for the free tier.
- You can add a custom domain later if you want (paid).

That’s it. Open the URL every morning and hit Refresh.