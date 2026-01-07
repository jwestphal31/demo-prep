# Demo Prep Tool - Mac App Launcher Guide

## 🚀 Quick Start

Two apps have been created in this folder:

### ▶️ **Start Demo Prep.app**
Double-click to start the web server
- Launches web interface at http://localhost:5001
- Opens browser automatically
- Shows notification when ready
- Safe to double-click multiple times (checks if already running)

### ■ **Stop Demo Prep.app**
Double-click to stop the web server
- Stops the background server
- Shows notification when stopped
- Safe to run even if server isn't running

## 📍 Location

Both apps are located at:
```
/Users/jwest/Documents/projects/demo-prep-tool/
```

## 🎨 Adding Custom Icons (Optional)

1. **Open Finder** and navigate to the demo-prep-tool folder
2. **Right-click** on "Start Demo Prep.app"
3. Select **"Get Info"**
4. **Drag** `start_icon.png` onto the small app icon in the top-left of the Info window
5. **Repeat** for "Stop Demo Prep.app" using `stop_icon.png`

## 🔖 Adding to Dock or Desktop

### Add to Dock:
1. Open Finder and navigate to the demo-prep-tool folder
2. **Drag** "Start Demo Prep.app" to your Dock
3. Now you can launch with one click!

### Add to Desktop:
1. Right-click on "Start Demo Prep.app"
2. Hold **Option** key
3. Select "Make Alias"
4. Drag the alias to your Desktop

### Add to Applications Folder (System-wide):
```bash
# Copy to Applications folder
sudo cp -r "Start Demo Prep.app" /Applications/
sudo cp -r "Stop Demo Prep.app" /Applications/

# Or create symlinks
ln -s "/Users/jwest/Documents/projects/demo-prep-tool/Start Demo Prep.app" /Applications/
ln -s "/Users/jwest/Documents/projects/demo-prep-tool/Stop Demo Prep.app" /Applications/
```

## 🎯 Usage

### Starting the Server

1. **Double-click** "Start Demo Prep.app"
2. You'll see a notification: *"Server started at http://localhost:5001"*
3. Browser opens automatically to the web interface
4. Start researching companies!

### Stopping the Server

1. **Double-click** "Stop Demo Prep.app"
2. You'll see a notification: *"Server stopped successfully"*
3. The web interface will no longer be accessible

## 📊 Checking Server Status

### Is the server running?
- Check for the file `.server.pid` in the demo-prep-tool folder
- Or double-click "Start Demo Prep.app" - it will tell you if already running
- Or visit http://localhost:5001 in your browser

### View Server Logs
Server logs are saved to `server.log` in the demo-prep-tool folder:
```bash
tail -f server.log
```

## 🔧 Troubleshooting

### Server won't start
1. Check `server.log` for errors
2. Make sure Python 3 is installed
3. Make sure Flask is installed: `pip3 install flask`
4. Check if port 5001 is available: `lsof -i :5001`

### Can't stop the server
1. Run "Stop Demo Prep.app" again
2. Or manually: `cat .server.pid` then `kill -9 <PID>`
3. Or: `pkill -f web_app.py`

### Notifications not showing
- Check System Settings → Notifications → Script Editor
- Make sure notifications are enabled

### Icons not working
- Manually apply icons using the steps above
- Or use the default app icon

## 🎨 Customizing

### Change the port
Edit `web_app.py` line 199:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5001 to another port
```

### Change startup behavior
Edit `start_server.sh` to customize:
- Remove `open http://localhost:5001` to not auto-open browser
- Change notification messages
- Add logging options

### Auto-start on login
1. Open **System Settings** → **General** → **Login Items**
2. Click the **+** button under "Open at Login"
3. Select "Start Demo Prep.app"
4. Server will start automatically when you log in

## 📁 Files Created

```
demo-prep-tool/
├── Start Demo Prep.app     # Launch app (double-click to start)
├── Stop Demo Prep.app      # Stop app (double-click to stop)
├── start_server.sh         # Start script (used by app)
├── stop_server.sh          # Stop script (used by app)
├── start_icon.png          # Blue play icon
├── stop_icon.png           # Red stop icon
├── .server.pid             # PID file (created when running)
└── server.log              # Server logs (created when running)
```

## 🚀 Advanced: Spotlight Search

Make the apps searchable via Spotlight:

1. Move or copy apps to `/Applications/` folder
2. They'll appear when you search "Demo Prep" in Spotlight (⌘ + Space)
3. Launch instantly with keyboard!

## ⌨️ Keyboard Shortcut (Optional)

Create a global keyboard shortcut:

1. **Open** System Settings → Keyboard → Keyboard Shortcuts
2. Select **App Shortcuts**
3. Click **+** to add new shortcut
4. Select "Start Demo Prep.app"
5. Assign a shortcut like **⌘ + Option + D**

Now press your shortcut to launch instantly!

## 🎉 You're All Set!

Just double-click "Start Demo Prep.app" to begin researching companies with the web interface!
