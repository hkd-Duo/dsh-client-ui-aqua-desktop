// Fails when a README mermaid block contains characters that GitHub's
// Mermaid parser rejects inside node labels: straight double quotes,
// smart quotes, unicode arrows, HTML line breaks, or emoji.
//
// GitHub renders mermaid client-side, so a parse error shows up as
// "Unable to render rich display" instead of a diagram. Keeping labels to
// plain text avoids that class of breakage.
import fs from 'node:fs'

const README = ['README.md', 'README.zh.md']
const BLOCK = /```mermaid\n([\s\S]*?)\n```/g
const BAD = /["\u201c\u201d\u2018\u2019\u2192\u2190\u2705\u274c\u26a0\u2318\u2b50]|<br/i

let failed = false
let blocks = 0

for (const file of README) {
  if (!fs.existsSync(file)) continue
  const src = fs.readFileSync(file, 'utf8')
  let index = 0
  for (const match of src.matchAll(BLOCK)) {
    index += 1
    blocks += 1
    match[1].split('\n').forEach((line, i) => {
      if (BAD.test(line)) {
        console.error(
          `FAIL ${file} block ${index} line ${i + 1}: forbidden character in mermaid label -> ${line.trim()}`,
        )
        failed = true
      }
    })
  }
  console.log(`${file}: ${index} mermaid block(s) checked`)
}

if (blocks === 0) {
  console.error('FAIL no mermaid blocks found; the diagrams were expected in the READMEs')
  failed = true
}

if (failed) {
  console.error('mermaid check failed: use plain text labels (no quotes, arrows, <br/> or emoji)')
  process.exit(1)
}
console.log(`mermaid check passed (${blocks} blocks)`)
