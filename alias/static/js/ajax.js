function getSelected() {
    var first = $('#custom_topics option:selected').map(function(a, item){return item.value;});
    var chosenOptions = [];
    var len;
    len = first.length;
    var i;
    for (i = 0; i < len; i++) {
        chosenOptions.push(first[i])
    }
    console.log(chosenOptions);
    return chosenOptions;
}


function startGame() {
    var postStart = {'action': 'start', 'topics': getSelected()};
    console.log(JSON.stringify((postStart)));
    $.ajax({
        type: 'POST',
        url: '/act',
        data: JSON.stringify(postStart),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (response) {
            console.log(response);
            getEnglish(response);
            getRussian(response);
        },
        failure: function () {
            console.log('fail');
        }
    })
}

function nextCard() {
    var postNew = {'action': 'next_card'};
    $.ajax({
        type: 'POST',
        url: '/action',
        data: JSON.stringify(postNew),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (response) {
            getEnglish(response);
            getRussian(response);
            console.log(response);
        },
        failure: function () {
            console.log('fail');
        }
    })
}

function prevCard() {
    var postPrev = {'action': 'prev_card'};
    $.ajax({
        type: 'POST',
        url: '/action',
        data: JSON.stringify(postPrev),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        cache: false,
        success: function (response) {
            getEnglish(response);
            getRussian(response);
            console.log(response);
        },
        failure: function () {
            console.log('fail');
        }
    })
}

function getEnglish(response) {
    clearWords("english");
    var englishWords = response.english;
    console.log(englishWords);
    var ul = document.createElement("ul");
    var i;
    for (i=0; i < 8; i++) {
        var li = document.createElement("li");
        var p = document.createElement("p");
        p.classList.add("translems");
        var word = document.createTextNode(englishWords[i]);
        p.appendChild(word);
        li.appendChild(p);
        ul.appendChild(li);
        console.log(englishWords[i])
    }
    var div = document.createElement("div");
    div.classList.add("container");
    div.appendChild(ul);
    var englishList = document.getElementById("english");
    englishList.appendChild(div);
}

function getRussian(response) {
    clearWords("russian");
    var russianWords = response.russian;
    console.log(russianWords);
    var ul = document.createElement("ul");
    var i;
    for (i=0; i < 8; i++) {
        var li = document.createElement("li");
        var p = document.createElement("p");
        p.classList.add("translems");
        var word = document.createTextNode(russianWords[i]);
        p.appendChild(word);
        li.appendChild(p);
        ul.appendChild(li);
        console.log(russianWords[i])
    }
    var div = document.createElement("div");
    div.classList.add("container");
    div.appendChild(ul);
    var englishList = document.getElementById("russian");
    englishList.appendChild(div);
}

function clearWords(parentId) {
    var parentNode = document.getElementById(parentId);
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}


