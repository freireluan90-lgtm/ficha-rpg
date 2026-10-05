from pathlib import Path

html_path=Path('app/src/main/assets/Ficha.html')
java_path=Path('app/src/main/java/br/com/luan/fichalivre/MainActivity.java')

s=html_path.read_text(encoding='utf-8')
s=s.replace('Versão instalada: <b>2.3</b> · cálculos automáticos de progressão','Versão instalada: <b>2.4</b> · atualizador nativo corrigido')
s=s.replace("const APP_VERSION='2.3';","const APP_VERSION='2.4';")
old="""$('#checkUpdate').onclick=async()=>{updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · procurando atualização…`);try{const r=await fetch(UPDATE_MANIFEST_URL+'?t='+Date.now(),{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);const d=await r.json();if(!d.version||!d.apk)throw new Error('manifesto inválido');updateState.latest=d;updateState.available=isNewer(d.version,APP_VERSION);updateState.downloaded=false;if(updateState.available){updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · disponível: <b>${d.version}</b>`);toast(`Nova versão ${d.version} encontrada.`)}else{updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · você já está na versão mais recente`);toast('Você já está na versão mais recente.')}}catch(e){updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · não foi possível consultar atualizações`);toast('Falha ao procurar atualizações. Verifique a internet.')}};"""
new="""async function readUpdateManifest(){if(window.AndroidFicha&&typeof AndroidFicha.fetchUpdateManifest==='function'){const raw=AndroidFicha.fetchUpdateManifest();const d=JSON.parse(raw||'{}');if(d.error)throw new Error(d.error);if(!d.version||!d.apk)throw new Error('manifesto inválido');return d}const r=await fetch(UPDATE_MANIFEST_URL+'?t='+Date.now(),{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);const d=await r.json();if(!d.version||!d.apk)throw new Error('manifesto inválido');return d}
$('#checkUpdate').onclick=async()=>{updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · procurando atualização…`);try{const d=await readUpdateManifest();updateState.latest=d;updateState.available=isNewer(d.version,APP_VERSION);updateState.downloaded=false;if(updateState.available){updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · disponível: <b>${d.version}</b>`);toast(`Nova versão ${d.version} encontrada.`)}else{updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · você já está na versão mais recente`);toast('Você já está na versão mais recente.')}}catch(e){updateMsg(`Versão instalada: <b>${APP_VERSION}</b> · não foi possível consultar atualizações`);toast('Falha ao procurar atualizações. Verifique a internet.')}};"""
if old not in s:
    raise SystemExit('checkUpdate original não encontrado')
s=s.replace(old,new,1)
html_path.write_text(s,encoding='utf-8')

j=java_path.read_text(encoding='utf-8')
for imp in [
    'import java.io.BufferedReader;\n',
    'import java.io.InputStreamReader;\n',
    'import java.net.HttpURLConnection;\n',
    'import java.net.URL;\n',
]:
    if imp not in j:
        j=j.replace('import java.io.OutputStream;\n', 'import java.io.OutputStream;\n'+imp, 1)

j=j.replace('@JavascriptInterface public String getAppVersion() { return "2.2"; }','@JavascriptInterface public String getAppVersion() { return "2.4"; }')
anchor='''        @JavascriptInterface public void downloadApk(String url, String version) {'''
method='''        @JavascriptInterface public String fetchUpdateManifest() {
            HttpURLConnection conn = null;
            try {
                URL u = new URL("https://raw.githubusercontent.com/freireluan90-lgtm/ficha-rpg/main/latest.json?t=" + System.currentTimeMillis());
                conn = (HttpURLConnection) u.openConnection();
                conn.setConnectTimeout(10000);
                conn.setReadTimeout(10000);
                conn.setUseCaches(false);
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Accept", "application/json");
                conn.setRequestProperty("User-Agent", "FichaLivre/" + getAppVersion());
                int code = conn.getResponseCode();
                if (code < 200 || code >= 300) return "{\\\"error\\\":\\\"http\\\"}";
                StringBuilder body = new StringBuilder();
                try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
                    char[] buf = new char[4096];
                    int n;
                    while ((n = in.read(buf)) != -1) {
                        body.append(buf, 0, n);
                        if (body.length() > 65536) return "{\\\"error\\\":\\\"manifest_too_large\\\"}";
                    }
                }
                JSONObject manifest = new JSONObject(body.toString());
                if (!manifest.has("version") || !manifest.has("apk")) return "{\\\"error\\\":\\\"invalid_manifest\\\"}";
                return manifest.toString();
            } catch (Exception e) {
                return "{\\\"error\\\":\\\"network\\\"}";
            } finally {
                if (conn != null) conn.disconnect();
            }
        }

'''
if 'fetchUpdateManifest()' not in j:
    if anchor not in j:
        raise SystemExit('âncora downloadApk não encontrada')
    j=j.replace(anchor,method+anchor,1)
java_path.write_text(j,encoding='utf-8')

assert "const APP_VERSION='2.4'" in s
assert 'readUpdateManifest' in s
assert 'fetchUpdateManifest()' in j
assert 'return "2.4"' in j
