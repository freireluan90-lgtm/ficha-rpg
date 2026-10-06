const { app, BrowserWindow, shell } = require('electron');
const path = require('path');

app.setName('Ficha Livre');

function createWindow() {
  const win = new BrowserWindow({
    width: 1180,
    height: 840,
    minWidth: 900,
    minHeight: 650,
    show: false,
    autoHideMenuBar: true,
    backgroundColor: '#111111',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  win.loadFile(path.join(__dirname, 'Ficha.html'));
  win.once('ready-to-show', () => win.show());

  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:/i.test(url)) shell.openExternal(url);
    return { action: 'deny' };
  });

  win.webContents.on('will-navigate', (event, url) => {
    if (/^https?:/i.test(url)) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });

  win.webContents.on('did-finish-load', () => {
    win.webContents.executeJavaScript(`
      (() => {
        const ids = ['downloadUpdate','installUpdate'];
        ids.forEach(id => { const b = document.getElementById(id); if (b) { b.disabled = true; b.style.display = 'none'; } });
        const check = document.getElementById('checkUpdate');
        if (check) { check.disabled = true; check.style.display = 'none'; }
        const st = document.getElementById('updateStatus');
        if (st) st.innerHTML = 'Versão PC: <b>3.6</b> · edição Windows portátil';
      })();
    `).catch(() => {});
  });
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
