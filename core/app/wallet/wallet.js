require("module-alias/register")

//const ... = require("@core/")
const ffi = require("ffi-napi")

const lib = ffi.Library("./libexample", {
  module_main_handler: ["str", ["str", "str"]]
})

const mdh = lib.module_main_handler

const fs = require("fs")

// 1.2.2 
// module wallet support 
// resiger and use wallet
let md = {}

function bapi() {
  const data = fs.readFileSync("api/rest", "utf8")
  const raw = json.Parse(data)
  md = raw
}
function _sign_user() {
  const msg_as_sign = md.msg 
  let table = { sign: msg_as_sign }
  if msg_as_sign.startsWith("*// ") {
    let user = md.sender 
    fs.writeFile(
      "database/.user/${user}.json",
      JSON.stringify(table, null, 2)
    )
    
  } else { 
      fs.writeFile(
        "database/log/report-extension-js.mph",
        ("Error: sign is wrong!") 
      )
  }
  
}
}

