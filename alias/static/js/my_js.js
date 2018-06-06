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
        document.querySelector('.control_timer').innerHTML = 'stop';
    } else if (window.isTimer === 1) {
        stopTimer();
        document.querySelector('.control_timer').innerHTML = 'resume';
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
    document.querySelector('.control_timer').innerHTML = 'start';
    showTimer();
}
// timer realization ends