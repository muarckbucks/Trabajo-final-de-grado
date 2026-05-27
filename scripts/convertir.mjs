// convertir.mjs
import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { DOMParser } from '@xmldom/xmldom';

const file = process.argv[2]; // node convertir.mjs imagen.svg
const svg = readFileSync(file, 'utf8');

// Extraer viewBox o width/height del SVG
const parser = new DOMParser();
const doc = parser.parseFromString(svg, 'image/svg+xml');
const root = doc.documentElement;
const [,, w, h] = (root.getAttribute('viewBox') || '').split(' ');
const width = parseFloat(w || root.getAttribute('width'));
const height = parseFloat(h || root.getAttribute('height'));

const browser = await puppeteer.launch();
const page = await browser.newPage();
await page.goto(`file://${process.cwd()}/${file}`);
await page.pdf({
  path: file.replace('.svg', '.pdf'),
  width: `${width}px`,
  height: `${height}px`,
  printBackground: true,
});
await browser.close();
console.log(`✓ ${file.replace('.svg', '.pdf')}`);

// Uso: node scripts/convertir.mjs imagenes-generacion/imagen.svg -> genera imagen.pdf
// es necesario: npm install puppeteer @xmldom/xmldom