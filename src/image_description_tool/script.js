let stats = {};
let allStats = [];
let allData;
let index = -1;

window.onload = async () => {
    let params = new URLSearchParams(window.location.search);
    let dataPath = params.get('data') ? params.get('data') : 'data.json';

    let response = await fetch(dataPath);
    allData = await response.json();

    document.addEventListener('keydown', (e) => {
        if (e.code == 'Enter') {
            this.submitDescription();
        }
    });

    document.getElementById('ctx_url').addEventListener('click', (e) => {if (!stats.clickSourceTime) stats.clickSourceTime = new Date().getTime();});

    document.addEventListener('blur', () => {
        if (!stats.leftWindowTime) stats.leftWindowTime = new Date().getTime();
    });
    
    showNextEntry();
}

function clearFields() {
    stats = {};
    
    // hide revealed content
    document.getElementById('ctx').hidden = true;

    // clear the input field
    document.getElementById('user_description').value = "";

    // clear tags
    let ctxTags = document.getElementById('ctx_tags');
    while (ctxTags.firstChild) {
        ctxTags.removeChild(ctxTags.firstChild);
    }

    let imgTags = document.getElementById('img_tags');
    while (imgTags.firstChild) {
        imgTags.removeChild(imgTags.firstChild);
    }
}

function showNextEntry() {
    index += 1;
    clearFields();

    if (index >= allData.length) {
        console.log('completed final task! Showing finished view.');
        document.getElementById('task-view').hidden = true;
        document.getElementById('finished-view').hidden = false;

        document.getElementById('result-object-final').innerText = JSON.stringify(allStats, undefined, 2);
        return;
    }

    let data = allData[index];

    // place all values into the correct HTML fields
    console.log(data);
    console.log(Object.keys(data));
    for (let key of Object.keys(data)) {
        if (data[key] instanceof Array) {
            // append with font size depending on relative score
            let minScore = data[key][data[key].length - 1].score;
            let maxScore = data[key][0].score;
            let fontSizes = data[key].map((entry, index) => {
                return mapNumberToRange(entry.score, minScore, maxScore, 16, 28) + 'px';
            });

            // create and append list items
            let items = data[key].map((entry, index) => {
                let listItem = document.createElement('li');
                console.log('setting font size of', entry.tag, 'to', fontSizes[index]);
                listItem.style.fontSize = fontSizes[index];
                listItem.appendChild(document.createTextNode(entry.tag));
                return listItem;
            });

            items.forEach((item) => {
                document.getElementById(key).appendChild(item);
            });
        } else if (key.includes('url')) {
            document.getElementById(key).href = data[key];
        } else if (key === 'img') {
            // image is source
            document.getElementById('img').src = data[key];
        } else {
            // just set the inner text
            document.getElementById(key).innerText = data[key];
        }
    }

    document.getElementById('submit_button').className = "btn btn-info";

    // start the timer
    stats.title = data['ctx_title'];
    stats.startTime = new Date().getTime();
}

function revealOrHideAutomaticDescription() {
    const descriptionButton = document.getElementById('button-show-description');
    const caption = document.getElementById('img_caption');
    console.log('Toggling description!');
    caption.hidden = !caption.hidden;

    // set button text appropriately
    descriptionButton.innerText = caption.hidden ? 'Klik om te tonen' : 'Klik om te verbergen';

    // timestamp is only set the first time
    if (!stats.revealDescriptionTime) stats.revealDescriptionTime = new Date().getTime();
}

function showOrHideFullContext() {
    const contextButton = document.getElementById('button-show-context');
    const context = document.getElementById('ctx');
    console.log('Toggling context!');
    context.hidden = !context.hidden;

    // set button text appropriately
    contextButton.innerText = context.hidden ? 'Klik om te tonen' : 'Klik om te verbergen';

    // timestamp is only set the first time
    if (!stats.revealContextTime) stats.revealContextTime = new Date().getTime();
}

function showCopyWarningToast() {
    console.warn('showing copy warning toast');

    if (!stats.attemptCopyTime) stats.attemptCopyTime = new Date().getTime();

    $('#toast-warn-copy').toast('show');
        setTimeout(() => {
            $('#toast-warn-copy').toast('hide');
        }, 2000);
    navigator.clipboard.writeText('');    
    return false;
}

async function submitDescription() {
    let description = document.getElementById('user_description').value;
    if (!description || description.length < 2) {
        console.warn('Submitted description was not present or too short!');
        $('#toast-warn-short').toast('show');
        setTimeout(() => {
            $('#toast-warn-short').toast('hide');
        }, 2000);
        return;
    }

    document.getElementById('submit_button').className = "btn btn-success";

    console.log('Submitting description');
    stats.endTime = new Date().getTime();
    stats.description = description;

    allStats.push(stats);

    showNextEntry();
}

// utility function to map numbers (for font size)
// retrieved from https://gist.github.com/xposedbones/75ebaef3c10060a3ee3b246166caab56
function mapNumberToRange(number, in_min, in_max, out_min, out_max) {
  return Math.round((number - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}

function downloadData() {
    console.log('downloading json...');

    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(allStats)));
    element.setAttribute('download', 'result.json');

    // add the new element to the page
    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function copyData() {
    navigator.clipboard.writeText(JSON.stringify(allStats));
    $('#toast-copy').toast('show');
        setTimeout(() => {
            $('#toast-copy').toast('hide');
        }, 2000);
}
