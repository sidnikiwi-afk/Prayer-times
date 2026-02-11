// Shared masjid navigation - edit this list to add/remove mosques
const MASJIDS = [
    { name: 'Shahjalal Islamic Society', addr: '149A Little Horton Lane, BD5 0HS', folder: 'shahjalal' },
    { name: 'Masjid Quba', addr: '20 Quba Court, BD8 7LA', folder: 'quba' },
    { name: 'Al Mahad Ul Islami', addr: 'Dorset Street, BD5 0LT', folder: 'Almahad' },
    { name: 'Tawakkulia Islamic Society', addr: '48 Cornwall Road, BD8 7JN', folder: 'Tawakkulia' },
];

(function() {
    // Detect current mosque from URL
    const path = window.location.pathname;
    const currentFolder = MASJIDS.find(m => path.includes('/' + m.folder + '/'));
    const isHome = !currentFolder;
    const pathPrefix = isHome ? '' : '../';

    // Inject CSS
    const style = document.createElement('style');
    style.textContent = `
        .masjid-nav {
            display: flex; align-items: center; justify-content: space-between;
            background: #1a1a2e; padding: 6px 12px; font-size: 12px;
        }
        .masjid-nav .nav-left { display: flex; align-items: center; gap: 8px; }
        .masjid-nav .nav-label {
            color: rgba(255,255,255,0.4); font-size: 10px;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .nav-selector { position: relative; }
        .nav-current {
            display: flex; align-items: center; gap: 6px;
            color: white; background: rgba(255,255,255,0.12);
            padding: 5px 12px; border-radius: 6px; cursor: pointer;
            font-size: 13px; font-weight: 600;
            border: 1px solid rgba(255,255,255,0.15);
            transition: all 0.2s ease; user-select: none;
        }
        .nav-current:hover { background: rgba(255,255,255,0.18); }
        .nav-current::after { content: '\\25BE'; font-size: 10px; opacity: 0.6; margin-left: 2px; }
        .nav-dropdown {
            display: none; position: absolute; top: calc(100% + 6px); left: 0;
            background: #1a1a2e; border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px; min-width: 280px; max-height: 360px;
            overflow-y: auto; z-index: 200; box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        }
        .nav-dropdown.open { display: block; }
        .nav-search {
            width: 100%; padding: 10px 12px; border: none;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.05); color: white;
            font-size: 13px; outline: none; border-radius: 8px 8px 0 0;
        }
        .nav-search::placeholder { color: rgba(255,255,255,0.3); }
        .nav-list { list-style: none; padding: 4px 0; }
        .nav-list a {
            display: flex; flex-direction: column; padding: 10px 14px;
            color: rgba(255,255,255,0.7); text-decoration: none;
            transition: all 0.15s ease; border-left: 3px solid transparent;
        }
        .nav-list a:hover { background: rgba(255,255,255,0.08); color: white; }
        .nav-list a.active {
            color: white; background: rgba(255,255,255,0.06);
            border-left-color: currentColor; font-weight: 600;
        }
        .nav-list .nav-name { font-size: 13px; }
        .nav-list .nav-addr { font-size: 10px; opacity: 0.45; margin-top: 1px; }
        .nav-all {
            display: block; text-align: center; padding: 8px;
            color: rgba(255,255,255,0.4); text-decoration: none;
            font-size: 11px; border-top: 1px solid rgba(255,255,255,0.08);
            transition: all 0.15s ease;
        }
        .nav-all:hover { color: white; background: rgba(255,255,255,0.05); }
        body.dark-mode .masjid-nav { background: #111122; }
        body.dark-mode .nav-dropdown { background: #111122; }
        @media print { .masjid-nav, .nav-dropdown { display: none !important; } }
    `;
    document.head.appendChild(style);

    // Build nav HTML
    const items = MASJIDS.map(m => {
        const isActive = currentFolder && m.folder === currentFolder.folder;
        return `<li><a href="${pathPrefix}${m.folder}/"${isActive ? ' class="active"' : ''}><span class="nav-name">${m.name}</span><span class="nav-addr">${m.addr}</span></a></li>`;
    }).join('');

    const nav = document.createElement('nav');
    nav.className = 'masjid-nav';
    nav.innerHTML = `
        <div class="nav-left">
            <span class="nav-label">Masjid</span>
            <div class="nav-selector">
                <div class="nav-current" id="navToggle">${currentFolder ? currentFolder.name : 'Select Masjid'}</div>
                <div class="nav-dropdown" id="navDropdown">
                    <input type="text" class="nav-search" id="navSearch" placeholder="Search masjids...">
                    <ul class="nav-list" id="navList">${items}</ul>
                    ${isHome ? '' : '<a href="../" class="nav-all">View all masjids</a>'}
                </div>
            </div>
        </div>
    `;

    // Insert nav as first child of .container
    const container = document.querySelector('.container');
    if (container) container.insertBefore(nav, container.firstChild);

    // Event handlers
    document.getElementById('navToggle').addEventListener('click', function() {
        const dd = document.getElementById('navDropdown');
        dd.classList.toggle('open');
        if (dd.classList.contains('open')) {
            const search = document.getElementById('navSearch');
            search.value = '';
            filterNav();
            setTimeout(function() { search.focus(); }, 50);
        }
    });

    document.getElementById('navSearch').addEventListener('input', filterNav);

    function filterNav() {
        const q = document.getElementById('navSearch').value.toLowerCase();
        document.querySelectorAll('#navList li').forEach(function(li) {
            li.style.display = li.textContent.toLowerCase().includes(q) ? '' : 'none';
        });
    }

    document.addEventListener('click', function(e) {
        var dd = document.getElementById('navDropdown');
        if (dd && !e.target.closest('.nav-selector')) dd.classList.remove('open');
    });
})();
