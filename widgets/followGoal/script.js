const options = document.styleOptions;

function runModule() {
    /** DO NOT MODIFY!!! USE OPTIONS.JS */
    const followerGoal = options.followerGoal;
    const followerGoalMessage = options.followerGoalMessage;
    var followerCount = 0;
    var goal = 0;
    function intervalFetch() {
        fetch(`https://ifuckinghatecors.herokuapp.com/https://apiv3.fansly.com/api/v1/account?usernames=${options.username}`)
        .then(data=> data.json())
        .then(d => {
            d = d.response[0]
            followerCount = d.followCount;
            goal = Math.round(followerCount/followerGoal);
            document.getElementById("feed").innerHTML = `
<div class="goalMessage">${followerGoalMessage}</div>
<div class="progressText">${followerCount}/${followerGoal}</div>
<progress value="${followerCount}" max=${followerGoal}></progress>
<div class="goalLeft">0</div>
<div class="goalRight">${followerGoal}</div>
`;
            
        })
    }
    intervalFetch();
    setInterval(intervalFetch, 500);
}

function loadOptions() {
    var newFontStyleSheet = document.createElement("style");
    
    let fontName = options.fontFile.split(".")[0];
    var font = new FontFace(`${fontName}`, `url("${options.fontFile}")`)
    font.load().then(function(loaded_face) {
        document.fonts.add(loaded_face)
        newFontStyleSheet.textContent = `
        body {
            margin: 0;
            font-size: 22px;
            color: #ffffff;
            font-family: ${fontName};
        }
        progress[value]::-webkit-progress-value {
            background-color: ${options.defaultBarColor};
        }
        `;
        document.head.appendChild(newFontStyleSheet);
        document.head.removeChild(document.getElementById('configurableOptions'));
    });
}

function onLoad() {
    loadOptions();
    runModule();
}