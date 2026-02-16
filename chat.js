(function () {
    'use strict';

    var WEBHOOK_URL = 'https://primary-production-64370.up.railway.app/webhook/prayer-chat';
    var MOSQUES = [
        { name: 'Shahjalal', folder: 'shahjalal' },
        { name: 'Masjid Quba', folder: 'quba' },
        { name: 'Al Mahad', folder: 'Almahad' },
        { name: 'Tawakkulia', folder: 'Tawakkulia' },
        { name: 'Salahadin', folder: 'Salahadin' },
        { name: 'Abu Bakar', folder: 'abubakar' },
        { name: 'IYMA', folder: 'iyma' },
        { name: 'Jamia Masjid', folder: 'JamiaMasjid' }
    ];
    var SUGGESTIONS = ['Latest Isha Jamaah?', 'Earliest Fajr Jamaah?'];

    var pathname = window.location.pathname;
    var currentMosque = MOSQUES.find(function (m) { return pathname.includes('/' + m.folder + '/'); });
    var isLanding = !currentMosque;
    var themeColor = (document.querySelector('meta[name="theme-color"]') || {}).content || '#004d40';

    var chatOpen = false;
    var contextCache = null;
    var sending = false;

    // --- Inject CSS ---
    var style = document.createElement('style');
    style.textContent = '\
.chat-btn{\
    position:fixed;bottom:140px;left:20px;width:50px;height:50px;border-radius:50%;\
    background:linear-gradient(135deg,#FFB300,#FF8F00);color:#fff;border:none;font-size:22px;cursor:pointer;\
    z-index:100;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);\
    box-shadow:0 4px 15px rgba(255,179,0,.4);transition:all .3s ease;\
    display:flex;align-items:center;justify-content:center;\
}\
.chat-btn:hover{transform:scale(1.1);box-shadow:0 6px 20px rgba(255,179,0,.6)}\
.chat-btn.open{display:none}\
.chat-panel{\
    position:fixed;bottom:20px;left:20px;width:340px;max-height:480px;\
    background:rgba(30,30,45,.95);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);\
    border-radius:20px;border:1px solid rgba(255,255,255,.1);\
    box-shadow:0 8px 32px rgba(0,0,0,.4);z-index:10001;\
    display:none;flex-direction:column;overflow:hidden;\
}\
.chat-panel.open{display:flex;animation:chatUp .3s ease}\
@keyframes chatUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}\
.chat-hdr{\
    display:flex;align-items:center;justify-content:space-between;\
    padding:14px 16px;background:' + themeColor + ';color:#fff;\
}\
.chat-hdr-title{font-size:14px;font-weight:600}\
.chat-close{background:none;border:none;color:#fff;font-size:20px;cursor:pointer;padding:0;line-height:1;opacity:.8}\
.chat-close:hover{opacity:1}\
.chat-msgs{flex:1;overflow-y:auto;padding:12px;min-height:200px;max-height:300px}\
.chat-msg{margin-bottom:10px;max-width:85%;padding:10px 14px;border-radius:16px;font-size:13px;line-height:1.5;word-wrap:break-word}\
.chat-msg.user{background:' + themeColor + ';color:#fff;margin-left:auto;border-bottom-right-radius:4px}\
.chat-msg.ai{background:rgba(255,255,255,.1);color:#e0e0e0;border-bottom-left-radius:4px}\
.chat-msg.loading{color:#999;font-style:italic}\
.chat-chips{display:flex;gap:6px;padding:0 12px 10px;flex-wrap:wrap}\
.chat-chip{\
    background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);\
    color:#ccc;padding:6px 12px;border-radius:20px;font-size:12px;cursor:pointer;transition:all .2s;\
}\
.chat-chip:hover{background:' + themeColor + '44;border-color:' + themeColor + ';color:#fff}\
.chat-input-row{display:flex;padding:10px 12px;border-top:1px solid rgba(255,255,255,.1);gap:8px}\
.chat-input{\
    flex:1;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);\
    border-radius:20px;padding:8px 14px;color:#fff;font-size:13px;outline:none;font-family:inherit;\
}\
.chat-input::placeholder{color:#888}\
.chat-input:focus{border-color:' + themeColor + '}\
.chat-send{\
    background:' + themeColor + ';border:none;color:#fff;width:36px;height:36px;\
    border-radius:50%;cursor:pointer;font-size:16px;\
    display:flex;align-items:center;justify-content:center;transition:opacity .2s;\
}\
.chat-send:disabled{opacity:.4;cursor:default}\
@media(max-width:400px){.chat-panel{left:10px;right:10px;width:auto;bottom:10px}}\
';
    document.head.appendChild(style);

    // --- Build UI ---
    var btn = document.createElement('button');
    btn.className = 'chat-btn';
    btn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><circle cx="9" cy="10" r="1" fill="#fff" stroke="none"/><circle cx="15" cy="10" r="1" fill="#fff" stroke="none"/></svg>';
    btn.title = 'Ask about prayer times';
    btn.addEventListener('click', function () { toggle(true); });
    document.body.appendChild(btn);

    var panel = document.createElement('div');
    panel.className = 'chat-panel';
    panel.innerHTML = '\
<div class="chat-hdr">\
    <span class="chat-hdr-title">Prayer Times Assistant</span>\
    <button class="chat-close">&times;</button>\
</div>\
<div class="chat-msgs" id="chatMsgs">\
    <div class="chat-msg ai">Assalamu alaykum! Ask me anything about prayer times across Bradford mosques.</div>\
</div>\
<div class="chat-chips" id="chatChips">' +
        SUGGESTIONS.map(function (s) { return '<button class="chat-chip">' + s + '</button>'; }).join('') +
'</div>\
<div class="chat-input-row">\
    <input class="chat-input" id="chatInput" placeholder="Ask about prayer times..." autocomplete="off">\
    <button class="chat-send" id="chatSend">\u27A4</button>\
</div>';
    document.body.appendChild(panel);

    var msgContainer = panel.querySelector('#chatMsgs');
    var input = panel.querySelector('#chatInput');
    var sendBtn = panel.querySelector('#chatSend');
    var chipsEl = panel.querySelector('#chatChips');

    panel.querySelector('.chat-close').addEventListener('click', function () { toggle(false); });
    panel.querySelectorAll('.chat-chip').forEach(function (c) {
        c.addEventListener('click', function () { sendMessage(c.textContent); });
    });
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(input.value); }
    });
    sendBtn.addEventListener('click', function () { sendMessage(input.value); });

    function toggle(open) {
        chatOpen = open;
        panel.classList.toggle('open', open);
        btn.classList.toggle('open', open);
        if (open) input.focus();
    }

    // --- Timetable context ---
    function getTodayRow(data) {
        var now = new Date();
        return data.find(function (d) {
            return d.date[0] === now.getFullYear() && d.date[1] === now.getMonth() + 1 && d.date[2] === now.getDate();
        });
    }

    function formatRow(name, row) {
        if (!row) return name + ': No data for today';
        var s = name + ': Sehri ' + row.sehri + ', Fajr ' + row.fajr + ' (Jamaah ' + row.jFajr + ')';
        s += ', Sunrise ' + row.sunrise;
        s += ', Zuhr ' + row.zuhr + ' (Jamaah ' + (row.jZuhl || row.jZuhr) + ')';
        s += ', Asr ' + row.asr + ' (Jamaah ' + row.jAsr + ')';
        s += ', Maghrib ' + row.maghrib;
        s += ', Isha ' + row.isha + ' (Jamaah ' + row.jIsha + ')';
        if (row.no) s += ', Ramadan Day ' + row.no;
        return s;
    }

    function getContext() {
        if (contextCache) return Promise.resolve(contextCache);

        var lines = [];

        // Current page data
        if (window.timetableData && currentMosque) {
            lines.push(formatRow(currentMosque.name, getTodayRow(window.timetableData)));
        }

        // Fetch other mosques
        var others = MOSQUES.filter(function (m) { return !currentMosque || m.folder !== currentMosque.folder; });
        var fetches = others.map(function (m) {
            var url = (isLanding ? '' : '../') + m.folder + '/index.html';
            return fetch(url).then(function (r) { return r.text(); }).then(function (html) {
                var match = html.match(/const\s+timetableData\s*=\s*(\[[\s\S]*?\]);\s*\n/);
                if (match) {
                    var data = new Function('return ' + match[1])();
                    return formatRow(m.name, getTodayRow(data));
                }
                return null;
            }).catch(function () { return null; });
        });

        return Promise.all(fetches).then(function (results) {
            results.forEach(function (r) { if (r) lines.push(r); });
            contextCache = lines.join('\n');
            return contextCache;
        });
    }

    // --- Messaging ---
    function addMsg(text, cls) {
        var el = document.createElement('div');
        el.className = 'chat-msg ' + cls;
        el.textContent = text;
        msgContainer.appendChild(el);
        msgContainer.scrollTop = msgContainer.scrollHeight;
        return el;
    }

    function sendMessage(text) {
        text = (text || '').trim();
        if (!text || sending) return;
        sending = true;
        input.value = '';
        sendBtn.disabled = true;
        if (chipsEl) { chipsEl.style.display = 'none'; }

        addMsg(text, 'user');
        var loadEl = addMsg('Thinking...', 'ai loading');

        getContext().then(function (ctx) {
            return fetch(WEBHOOK_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text, context: ctx })
            });
        }).then(function (res) { return res.json(); }).then(function (data) {
            loadEl.textContent = data.answer || data.output || 'Sorry, I could not get an answer.';
            loadEl.classList.remove('loading');
        }).catch(function () {
            loadEl.textContent = 'Sorry, something went wrong. Please try again.';
            loadEl.classList.remove('loading');
        }).finally(function () {
            sending = false;
            sendBtn.disabled = false;
            input.focus();
        });
    }
})();
