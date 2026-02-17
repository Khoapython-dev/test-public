const fs = require("fs")

class Transaction {
  constructor() {
    const apiData = this._getAPI()
    const cwp = this._getColdWallet()

    this.From = apiData.sender
    this.To = apiData.claimer
    this.Message = apiData.msg
    this.Amount = Number(apiData.amount) // ép kiểu cho chắc

    this.dict_table = cwp

    this._transfer()
  }

  _getAPI() {
    try {
      const api = fs.readFileSync("api/rest", "utf8")
      return JSON.parse(api)
    } catch (err) {
      throw new Error("API read error")
    }
  }

  _getColdWallet() {
    try {
      const cw = fs.readFileSync(
        "core/source/data/_.coldwallet.json",
        "utf8"
      )
      return JSON.parse(cw)
    } catch (err) {
      return {}
    }
  }

  _transfer() {
    const pathFrom = `database/.user/${this.From}.json`
    const pathTo   = `database/.user/${this.To}.json`

    if (!fs.existsSync(pathFrom) || !fs.existsSync(pathTo)) {
      throw new Error("User not found")
    }

    const r1 = JSON.parse(fs.readFileSync(pathFrom, "utf8"))
    const r2 = JSON.parse(fs.readFileSync(pathTo, "utf8"))

    if (r1.amount < this.Amount) {
      throw new Error("Insufficient balance")
    }

    r1.amount -= this.Amount
    r2.amount += this.Amount

    fs.writeFileSync(pathFrom, JSON.stringify(r1, null, 2))
    fs.writeFileSync(pathTo, JSON.stringify(r2, null, 2))

    console.log("Transfer success")
  }
}

new Transaction()