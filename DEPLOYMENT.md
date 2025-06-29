# 🚀 Deployment Guide: STL Weight Estimator API

This guide will walk you through deploying your STL Weight Estimator API to Render so it can be used by anyone on the internet!

## 📋 Prerequisites

1. **GitHub Account** - You'll need to push your code to GitHub
2. **Render Account** - Sign up at [render.com](https://render.com) (free)
3. **Your Code** - The STL Weight Estimator API files

## 🔧 Step 1: Prepare Your Code

### 1.1 Push to GitHub

First, create a new GitHub repository and push your code:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: STL Weight Estimator API"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 1.2 Verify Your Files

Make sure you have these files in your repository:
- ✅ `main.py` - Main FastAPI application
- ✅ `requirements.txt` - Python dependencies (updated for Python 3.11+)
- ✅ `render_start.py` - Production startup script
- ✅ `test.html` - Web interface
- ✅ `README.md` - Documentation

## 🌐 Step 2: Deploy to Render

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Get Started" and sign up with your GitHub account
3. Render will automatically connect to your GitHub repositories

### 2.2 Create New Web Service

1. **Click "New +"** in your Render dashboard
2. **Select "Web Service"**
3. **Connect your GitHub repository** (if not already connected)
4. **Select your STL Weight Estimator repository**

### 2.3 Configure the Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `stl-weight-estimator` (or any name you like) |
| **Environment** | `Python 3` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python render_start.py` |
| **Plan** | `Free` |

### 2.4 Advanced Settings (Optional)

Click "Advanced" and add these environment variables if needed:

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `production` | Sets production mode |
| `PYTHON_VERSION` | `3.11.7` | Specifies Python version |

### 2.5 Deploy!

1. **Click "Create Web Service"**
2. **Wait for deployment** (usually 2-5 minutes)
3. **Your API will be live!** 🎉

## 🔗 Step 3: Access Your Deployed API

Once deployed, you'll get a URL like:
```
https://your-app-name.onrender.com
```

### Available Endpoints:

- **API Documentation**: `https://your-app-name.onrender.com/docs`
- **Test Interface**: `https://your-app-name.onrender.com/test`
- **Health Check**: `https://your-app-name.onrender.com/health`
- **Weight Estimation**: `https://your-app-name.onrender.com/estimate-weight`

## 🧪 Step 4: Test Your Deployed API

### 4.1 Test with curl

```bash
curl -X POST "https://your-app-name.onrender.com/estimate-weight" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your-model.stl" \
  -F "infill_percentage=20" \
  -F "material_density=1.24" \
  -F "line_thickness=0.4"
```

### 4.2 Test with the Web Interface

1. Open `https://your-app-name.onrender.com/test`
2. Upload an STL file
3. Set your printing parameters
4. Click "Estimate Weight"

### 4.3 Test with Python

```python
import requests

url = "https://your-app-name.onrender.com/estimate-weight"
files = {"file": open("model.stl", "rb")}
data = {
    "infill_percentage": 20,
    "material_density": 1.24,
    "line_thickness": 0.4
}

response = requests.post(url, files=files, data=data)
result = response.json()
print(f"Weight: {result['weight_grams']} grams")
```

## 📊 Step 5: Monitor Your API

### 5.1 Render Dashboard

- **Logs**: View real-time logs in your Render dashboard
- **Metrics**: Monitor CPU, memory, and request count
- **Deployments**: See deployment history and status

### 5.2 Health Monitoring

Your API includes a health endpoint:
```bash
curl https://your-app-name.onrender.com/health
```

## 🔧 Step 6: Custom Domain (Optional)

### 6.1 Add Custom Domain

1. Go to your service settings in Render
2. Click "Custom Domains"
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update your DNS records as instructed

### 6.2 Update Test Page

If you add a custom domain, update the test page URL detection.

## 🚨 Troubleshooting

### Common Issues:

1. **Build Fails with "Cannot import 'setuptools.build_meta'"**
   - **Solution**: The requirements.txt has been updated to use Python 3.11+ compatible versions
   - **Alternative**: Use `requirements-render.txt` instead by changing the build command to `pip install -r requirements-render.txt`

2. **Build Fails**
   - Check `requirements.txt` for correct dependencies
   - Verify Python version compatibility (use Python 3.11.7)
   - Try using the build script: `chmod +x build.sh && ./build.sh`

3. **API Not Responding**
   - Check Render logs for errors
   - Verify the start command is correct

4. **CORS Errors**
   - The API includes CORS middleware for cross-origin requests
   - Check browser console for specific errors

5. **File Upload Issues**
   - Ensure STL files are valid
   - Check file size limits (Render has limits)

### Getting Help:

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Render Community**: [community.render.com](https://community.render.com)
- **Check Logs**: Always check the logs in your Render dashboard first

## 🎉 Success!

Your STL Weight Estimator API is now live and accessible to anyone on the internet! 

**Share your API URL**: `https://your-app-name.onrender.com`

**API Documentation**: `https://your-app-name.onrender.com/docs`

**Test Interface**: `https://your-app-name.onrender.com/test`

## 🔄 Updating Your API

To update your deployed API:

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update API"
   git push
   ```
3. Render will automatically redeploy your service

## 💰 Cost Management

- **Free Tier**: 750 hours/month (enough for continuous operation)
- **Sleep Mode**: Free tier services sleep after 15 minutes of inactivity
- **Wake Time**: First request after sleep takes 30-60 seconds to wake up

---

**Congratulations!** 🎉 Your STL Weight Estimator API is now publicly available and ready to use! 