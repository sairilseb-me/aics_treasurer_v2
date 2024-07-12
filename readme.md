# AICS Treasurer System

### This is a System for AICS Treasurer - Province of Guimaras

## Installation Procedure

**Run the XAMPP first before doing anything**

1. Clone the repository `https://github.com/sairilseb-me/aics_treasurer_v2.git`
2. Change directory to `cd aics_treasurer_v2`
3. Change directory to `cd backend` and open file `main.py`
4. Change the `host` to the IP Address of the Server and the `port` (preferably a vacant port)
``` if __name__ == '__main__':    
    app.run(host='<ip_address>'', port='<port>' debug=True)
```
5. Run `main.py`
6. Change directory to `frontend`
7. Run `npm install`
8. Change the `port` for the Frontend
```
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5174,
  }
})
```

9. Run `npm run build`, take note where your `dist` directory is
10. Go to `path/xampp/apache/conf/extra` 
11. Create a `.conf` file and the following
```
Listen <frontend port>

<VirtualHost *:<frontend port>>
    DocumentRoot "/path/to/xampp/htdocs/aics_treasurer_v2"
    <Directory "/path/to/xampp/htdocs/aics_treasurer_v2">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

```

12. `Include` the file to the `httpd.conf` file.
13. Restart the XAMPP
