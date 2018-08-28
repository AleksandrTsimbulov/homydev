function change_language() {
    var english, russian;
    english = $('#english').css('display');
    if (english === 'block') {
        $('#english').css('display', 'none');
        $('#russian').css('display', 'block');
    } else {
        $('#english').css('display', 'block');
        $('#russian').css('display', 'none');
    }
}

// time realization begins
function addHalfMinute() {
    if (window.totalSeconds < 570) {
        window.totalSeconds += 30;
        showTimer();
    }

    console.log(window.totalSeconds);
}

function subtractHalfMinute() {
    if (window.totalSeconds > 30) {
        window.totalSeconds -= 30;
        showTimer();
    }

    console.log(window.totalSeconds)
}

function getTime(seconds) {
    var sec = Math.floor( seconds % 60);
    var min = Math.floor( (seconds/60) % 60);
    return {
        'tot': seconds,
        'min': min,
        'sec': sec
    };
}

function showTimer() {
    var time = getTime(window.totalSeconds);
    var min = time.min;
    var sec = time.sec;
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
        console.log('in control');
        startTimer();
        document.querySelector('.control_timer').innerHTML = 'STOP';
    } else if (window.isTimer === 1) {
        stopTimer();
        document.querySelector('.control_timer').innerHTML = 'RESUME';
    } else {
        console.log('I do not know how I got here!');
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
    document.querySelector('.control_timer').innerHTML = 'START';
    showTimer();
}
// timer realization ends

// sound player
function play_time_is_over() {
    var sound = document.getElementById('end_sound');
    sound.play();
}

// make it fullscreen
function toggleFullScreen() {
    console.log('I am here!');
  var doc = window.document;
  var docEl = doc.documentElement;

  var requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
  var cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen || doc.msExitFullscreen;

  if(!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
    requestFullScreen.call(docEl);
  }
  else {
    cancelFullScreen.call(doc);
  }
}


var goFS = document.getElementById("full");
goFS.addEventListener("click", toggleFullScreen);