const fs = require('fs')
const path = require('path')
const wallet = require('./wallet')

// Prepare test input
fs.mkdirSync(path.join(__dirname, '..', '..', '..', 'api'), { recursive: true })
const apiPath = path.join(__dirname, 'api', '..', '..', 'api', 'rest')
// Simpler: write to project-relative api/rest used by wallet.bapi
fs.mkdirSync('api', { recursive: true })
fs.writeFileSync('api/rest', JSON.stringify({ msg: '*// signed', sender: 'alice' }), 'utf8')

// Run
try {
  wallet.bapi()
  wallet._sign_user()
  const userFile = 'database/.user/alice.json'
  if (fs.existsSync(userFile)) {
    console.log('OK: user file created: ' + userFile)
    console.log(fs.readFileSync(userFile, 'utf8'))
  } else {
    console.error('FAIL: user file not created')
  }
} catch (err) {
  console.error('Runtime error:', err.message)
}
