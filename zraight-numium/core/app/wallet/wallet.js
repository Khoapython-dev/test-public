try {
  require("module-alias/register")
} catch (e) {
  // ignore if module-alias is not installed in this environment
}

let mdh = null
const fs = require("fs")

try {
  const ffi = require("ffi-napi")
  const lib = ffi.Library("./libexample", {
    module_main_handler: ["string", ["string", "string"]]
  })
  mdh = lib.module_main_handler
} catch (e) {
  // ffi-napi or native lib may be unavailable in this environment.
  // Provide a stub that throws when used so module can still be required.
  mdh = function () {
    throw new Error("ffi module or native library not available: " + e.message)
  }
}

// module wallet support
// register and use wallet
let md = {}

function bapi() {
  try {
    const data = fs.readFileSync("api/rest", "utf8")
    const raw = JSON.parse(data)
    md = raw
  } catch (err) {
    try {
      fs.mkdirSync("database/log", { recursive: true })
      fs.writeFileSync(
        "database/log/report-extension-js.mph",
        `Error parsing api/rest: ${err.message}`,
        "utf8"
      )
    } catch (e) {
      // swallow secondary errors to avoid crashing on logging
    }
  }
}

function _sign_user() {
  const msg_as_sign = md.msg
  const table = { sign: msg_as_sign }

  if (typeof msg_as_sign === "string" && msg_as_sign.startsWith("*// ")) {
    const user = md.sender
    try {
      fs.mkdirSync("database/.user", { recursive: true })
      fs.writeFileSync(
        `database/.user/${user}.json`,
        JSON.stringify(table, null, 2),
        "utf8"
      )
    } catch (err) {
      fs.mkdirSync("database/log", { recursive: true })
      fs.writeFileSync(
        "database/log/report-extension-js.mph",
        `Error writing user file: ${err.message}`,
        "utf8"
      )
    }
  } else {
    fs.mkdirSync("database/log", { recursive: true })
    fs.writeFileSync(
      "database/log/report-extension-js.mph",
      "Error: sign is wrong!",
      "utf8"
    )
  }
}

module.exports = { bapi, _sign_user, mdh }

