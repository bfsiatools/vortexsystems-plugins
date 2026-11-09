/* Teste de navegador da landing page (opcional; precisa de Playwright instalado: npm i -D playwright).
   Uso: node verificar-navegador.cjs CAMINHO/index.html [--chrome CAMINHO_DO_CHROME]
   Confere: sem rolagem horizontal em 320/390/820/1440 px, botao final clicavel (nada por cima), imagens carregadas,
   links do WhatsApp, ancora "proximos passos", video (se houver), pagina visivel sem JavaScript e com movimento reduzido.
   Nao envia mensagem, nao publica, nao abre servidor. */
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  if (!args[0]) { console.error('Uso: node verificar-navegador.cjs CAMINHO/index.html [--chrome CAMINHO]'); process.exit(2); }
  const url = pathToFileURL(path.resolve(args[0])).href;
  const i = args.indexOf('--chrome');
  const executablePath = process.env.CHROME || (i >= 0 ? args[i + 1] : undefined);
  const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
  try {
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(url);
    await page.evaluate(() => document.fonts.ready);
    assert.equal((await page.locator('body').innerText()).includes('{{'), false, 'placeholder sobrando');
    for (const width of [1440, 820, 390, 320]) {
      await page.setViewportSize({ width, height: 844 });
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, `Rolagem horizontal em ${width}px`);
      const cta = page.locator('.fecho .btn');
      await cta.scrollIntoViewIfNeeded();
      await page.waitForTimeout(900);
      assert.equal(await cta.evaluate(el => {
        const r = el.getBoundingClientRect();
        return [.1, .5, .9].every(f => { const hit = document.elementFromPoint(r.left + r.width * f, r.top + r.height / 2); return el === hit || el.contains(hit); });
      }), true, `Botao final bloqueado em ${width}px`);
    }
    assert.deepEqual(await page.evaluate(() => [...document.images].filter(im => !im.complete || !im.naturalWidth).map(im => im.src)), [], 'imagem quebrada');
    const numeros = new Set();
    for (const href of await page.locator('a[target="_blank"]').evaluateAll(ls => ls.map(l => l.href))) {
      const u = new URL(href);
      assert.equal(u.origin, 'https://wa.me');
      assert.match(u.pathname, /^\/55\d{10,11}$/);
      assert.ok(u.searchParams.get('text'));
      numeros.add(u.pathname);
    }
    assert.equal(numeros.size, 1, 'mais de um numero de WhatsApp na pagina');
    await page.locator('.hero .btn').click();
    assert.equal(new URL(page.url()).hash, '#proximos-passos');
    if (await page.locator('video').count()) {
      const v = await page.locator('video').evaluate(async el => {
        el.muted = true; await el.play(); el.currentTime = Math.min(5, el.duration / 2);
        await new Promise(r => el.addEventListener('seeked', r, { once: true })); el.pause();
        return { duration: el.duration, error: el.error ? el.error.message : null };
      });
      assert.equal(v.error, null, 'erro no video'); assert.ok(v.duration > 1);
    }
    await page.emulateMedia({ reducedMotion: 'reduce' });
    assert.equal(await page.locator('.reveal').first().evaluate(el => getComputedStyle(el).opacity), '1');
    const semJS = await browser.newPage({ javaScriptEnabled: false });
    await semJS.goto(url);
    assert.equal(await semJS.locator('.reveal').first().evaluate(el => getComputedStyle(el).opacity), '1', 'conteudo escondido sem JavaScript');
    assert.deepEqual(errors, [], 'erro de JavaScript na pagina');
    console.log(JSON.stringify({ status: 'OK', larguras: [1440, 820, 390, 320], whatsapp: [...numeros][0] }));
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e); process.exitCode = 1; });
