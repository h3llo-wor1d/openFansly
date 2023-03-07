function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const BASE_URL = "https://ifuckinghatecors.herokuapp.com/https://apiv3.fansly.com/api/v1";

class Fansly {
    constructor(username, password) {
        this.username = username;
        this.password = password;
        this.token = "";
        this.headers = {};
    }

    login = async () => {
        return new Promise((resolve, reject) => {
            let deviceID = makeid(7);
            let headers = {"Referer": "https://fansly.com","Content-Type": "application/json","Accept": "application/json","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}
            fetch(`${BASE_URL}/login`, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({
                    deviceID: deviceID,
                    password: this.password,
                    username: this.username
                })
            })
            .then(resp => resp.json())
            .then(data => {
                if (data.success) {
                    let response = data.response;
                    if ("twofa" in response) {
                        // 2FA Auth Flow
                        console.log("Additional 2FA auth required.")
                        let code = prompt("What is the 2FA code you received via email?");
                        console.log(`Authenticating using code ${code}`);
                        fetch (`${BASE_URL}/login/twofa`, {
                            method: "POST",
                            headers: headers,
                            body: JSON.stringify({
                                token: response.twofa.token,
                                code: code
                            })
                        })
                        .then(resp => resp.json())
                        .then(data => {
                            console.log("Logged in successfully.")
                            this.token = data.response.token;
                            this.headers = {
                                "Referer": "https://fansly.com",
                                "Content-Type": "application/json",
                                "Accept": "application/json",
                                "Authorization": this.token,
                                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                            }
                            resolve();
                        })
                    } else {
                        // Normal auth flow
                        console.log("Logged in successfully.");
                        this.token = response.session.token;
                        this.headers = {
                            "Referer": "https://fansly.com",
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "Authorization": this.token,
                            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
                        }
                        resolve();
                    }
                }
            });
        })     
    }
}