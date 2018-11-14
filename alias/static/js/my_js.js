/////////////////////////////////////////////////////// timer begins

function addHalfMinute() {
    if (window.totalSeconds < 570) {
        window.totalSeconds += 30;
        showTimer();
    }
}

function subtractHalfMinute() {
    if (window.totalSeconds > 30) {
        window.totalSeconds -= 30;
        showTimer();
    }
}

function getTime(seconds) {
    let sec = Math.floor( seconds % 60);
    let min = Math.floor( (seconds/60) % 60);
    return {
        'tot': seconds,
        'min': min,
        'sec': sec
    };
}

function showTimer() {
    let time = getTime(window.totalSeconds);
    let min = time.min;
    let sec = time.sec;
    document.querySelector('.minutes').innerHTML = min.toString();
    document.querySelector('.seconds').innerHTML = sec.toString();
}

function startTimer() {
    if (window.totalSeconds <= 0 || window.isTimer === 1) {
        return;
    }
    window.isTimer = 1;
    window.isFirstStart = 0;
    window.timeInterval = setInterval(function () {
        window.totalSeconds -= 1;
        showTimer();
        if (window.totalSeconds <= 0) {
            play_time_is_over();
            stopTimer();
        }
    }, 1000);
}

function stopTimer() {
    window.isTimer = 0;
    clearInterval(window.timeInterval);
}

function controlTimer() {
    if (window.isFirstStart === 1 || window.isTimer === 0) {
        startTimer();
        document.querySelector('.control_timer').innerHTML = 'Stop timer';
    } else if (window.isTimer === 1) {
        stopTimer();
        document.querySelector('.control_timer').innerHTML = 'Resume timer';
    } else {
        console.log('fuction controlTimer error');
    }
}

function resetTimer() {
    if (window.isTimer === 1) {
        stopTimer();
    }
    initiate_timer();
}

function initiate_timer() {
    window.totalSeconds = 120;
    window.isFirstStart = 1;
    window.isTimer = 0;
    document.querySelector('.control_timer').innerHTML = 'Start timer';
    showTimer();
}
//////////////////////////////////////////////////////////// timer ends


/////////////////////////////////////////////////////////// navigation begins
function goToStudy() {
    window.location.pathname = '/study';
}

function goToFun() {
    window.location.pathname = '/for_fun';
}

function backToMenu() {
    window.location.pathname = '/welcome';
}

function logOut() {
    window.location.pathname = '/logout'
}
/////////////////////////////////////////////////////////// navigation ends


/////////////////////////////////////////////////////////// main control

var selectedTopics;
var currentLanguage;

function initiateTopicList() {
    selectedTopics = [];
}

function initiateLanguage() {
    currentLanguage = "english";
}

function change_language() {
    if (currentLanguage === "english") {
        currentLanguage = "russian";
        getRussian();
    } else {
        currentLanguage = "english";
        getEnglish();
    }
}

function quickStart() {
    let postQuickStart = {'action': 'add_topics', 'topics': ['regular_alias_words']};
    $.ajax({
        type: 'POST',
        url: '/act',
        data: JSON.stringify(postQuickStart),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function () {
            window.location.pathname = '/game';
        },
        failure: function () {
            console.log('quickStart failed');
        }
    });
}

function startGame() {
    let postStart = {'action': 'add_topics', 'topics': selectedTopics};
    console.log(JSON.stringify((postStart)));
    $.ajax({
        type: 'POST',
        url: '/act',
        data: JSON.stringify(postStart),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (response) {
            window.location.pathname = '/game';
        },
        failure: function () {
            console.log('startGame failed');
        }
    });
}

function selectTopic(elmnt) {
    let topic = elmnt.firstChild.textContent;
    topic = topic.split(' ').join('_');

    if (selectedTopics.includes(topic)) {
        selectedTopics.splice(selectedTopics.indexOf(topic), 1);
        elmnt.style.background = "#FFEDC2";
    }
    else {
        selectedTopics.push(topic);
        elmnt.style.background = "#ffc53d";
    }
    console.log(topic);
    console.log(selectedTopics)
}

function nextCard() {
    if (window.isTimer === 0) {
        resetTimer();
    }
    var postNew = {'action': 'next_card'};
    $.ajax({
        type: 'POST',
        url: '/act',
        data: JSON.stringify(postNew),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (response) {
            window.ajaxResponse = response;
            window.currentLanguage = "english";
            getEnglish();
        },
        failure: function () {
            console.log('nextCard fail');
        }
    })
}

function prevCard() {
    var postPrev = {'action': 'prev_card'};
    $.ajax({
        type: 'POST',
        url: '/act',
        data: JSON.stringify(postPrev),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (response) {
            window.ajaxResponse = response;
            window.currentLanguage = "english";
            getEnglish();
        },
        failure: function () {
            console.log('prevCard fail');
        }
    })
}

function getEnglish() {
    clearWords();
    let englishWords = window.ajaxResponse.english;
    let i;
    for (i=0; i < 8; i++) {
        document.getElementById((i+1).toString()).innerText = englishWords[i];
    }
}

function getRussian() {
    clearWords();
    let russianWords = window.ajaxResponse.russian;
    let i;
    for (i=0; i < 8; i++) {
        document.getElementById((i+1).toString()).innerText = russianWords[i];
    }
}

function clearWords() {
    let i;
    for (i=1; i < 9; i++) {
        let elem = document.getElementById(i.toString());
        elem.innerText = "";
    }
}

function toggleFullScreen() {
  // make it fullscreen and back
  let doc = window.document;
  let docEl = doc.documentElement;
  let button = document.getElementsByClassName('full_screen')[0];

  let requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
  let cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen;

  if(!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
    button.innerHTML = 'Exit f/screen';
    requestFullScreen.call(docEl);
  }
  else {
    cancelFullScreen.call(doc);
    button.innerHTML = 'Full screen';
  }
}

/////////////////////////////////////////////////////////////////// main control ends


////////////////////////////////////////////////////////////////// future functions

// sound player
function play_time_is_over() {
    let sound = document.getElementById('end_sound');
    sound.play();
}

function makeSoundVisible() {
    let soundImages = document.getElementsByClassName('sound');
    let i;
    for (i = 0; i < soundImages.length; i++) {
        soundImages[i].style.visibility = "visible";
    }
}


