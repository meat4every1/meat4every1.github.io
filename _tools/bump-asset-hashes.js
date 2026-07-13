/**
 * Cache-bust CSS/JS URLs in live HTML by content hash.
 * Usage: node _tools/bump-asset-hashes.js [--all]
 *   --all  also update Archive/**/*.html
 *
 * Lives under _tools/ so GitHub Pages (Jekyll) will not publish it.
 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const includeArchive = process.argv.includes('--all');

const assets = [
	{ file: 'style.css', attr: 'href' },
	{ file: 'colorbox.css', attr: 'href' },
	{ file: 'sidebar-loader.js', attr: 'src' },
];

function shortHash(filePath) {
	const buf = fs.readFileSync(filePath);
	return crypto.createHash('sha256').update(buf).digest('hex').slice(0, 8);
}

function listHtmlFiles() {
	const out = [];
	for (const name of fs.readdirSync(root)) {
		if (name.endsWith('.html')) out.push(path.join(root, name));
	}
	if (includeArchive) {
		const walk = (dir) => {
			for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
				const p = path.join(dir, ent.name);
				if (ent.isDirectory()) walk(p);
				else if (ent.name.endsWith('.html')) out.push(p);
			}
		};
		const arch = path.join(root, 'Archive');
		if (fs.existsSync(arch)) walk(arch);
	}
	return out;
}

const hashes = {};
for (const a of assets) {
	const fp = path.join(root, a.file);
	if (!fs.existsSync(fp)) {
		console.warn('skip missing', a.file);
		continue;
	}
	hashes[a.file] = shortHash(fp);
	console.log(a.file, '->', hashes[a.file]);
}

let filesChanged = 0;
for (const htmlPath of listHtmlFiles()) {
	let text = fs.readFileSync(htmlPath, 'utf8');
	const before = text;
	for (const a of assets) {
		const h = hashes[a.file];
		if (!h) continue;
		const esc = a.file.replace(/\./g, '\\.');
		const re = new RegExp(
			`(${a.attr}\\s*=\\s*")${esc}(?:\\?[^"]*)?(")`,
			'gi'
		);
		text = text.replace(re, `$1${a.file}?v=${h}$2`);
	}
	if (text !== before) {
		fs.writeFileSync(htmlPath, text, 'utf8');
		filesChanged++;
		console.log('updated', path.relative(root, htmlPath));
	}
}

console.log(filesChanged ? `Done. ${filesChanged} HTML file(s) updated.` : 'No HTML changes needed.');
