// Shared masjid navigation - edit this list to add/remove mosques
const MASJIDS = [
    { name: 'Shahjalal Islamic Society', addr: '149A Little Horton Lane, BD5 0HS', folder: 'shahjalal', tags: 'Bradford Little Horton' },
    { name: 'Masjid Quba', addr: '20 Quba Court, BD8 7LA', folder: 'quba', tags: 'Bradford Manningham' },
    { name: 'Al Mahad Ul Islami', addr: 'Dorset Street, BD5 0LT', folder: 'Almahad', tags: 'Bradford Little Horton' },
    { name: 'Tawakkulia Islamic Society', addr: '48 Cornwall Road, BD8 7JN', folder: 'Tawakkulia', tags: 'Bradford Manningham' },
    { name: 'Salahadin Mosque', addr: '62 Little Horton Lane, BD5 0BS', folder: 'Salahadin', tags: 'Bradford Little Horton' },
    { name: 'Masjid Abu Bakar', addr: '38 Steadman Terrace, BD3 9NB', folder: 'abubakar', tags: 'Bradford' },
    { name: 'IYMA', addr: '68 Idle Road, BD2 4NH', folder: 'iyma', tags: 'Bradford Idle' },
    { name: 'Jamia Masjid', addr: '28-32 Howard St, BD5 0BP', folder: 'JamiaMasjid', tags: 'Bradford' },
    { name: 'Masjid Taqwa', addr: '807 Great Horton Road, BD7 4AG', folder: 'taqwa', tags: 'Bradford Great Horton' },
    { name: 'Al Abrar Academy', addr: '10-20 Heap Lane, Bradford, BD3 0DT', folder: 'alabrar', tags: 'Bradford' },
    { name: 'Al Amin Islamic Society / Jamia Masjid & Madrasa', addr: 'Kensington Street, Keighley, BD21 1HZ', folder: 'alamin', tags: 'Bradford Keighley' },
    { name: 'Al Hidaya Academy', addr: 'Chapel Lane (Off Highgate Road), Queensbury, BD13 1EG', folder: 'alhidaya', tags: 'Bradford Queensbury' },
    { name: 'Masjid Al Hikmah & Learning Centre', addr: '181A Barkerend Rd, Bradford, BD3 9AP', folder: 'alhikmah', tags: 'Bradford' },
    { name: 'Al-Hidaayah Foundation', addr: 'Bridge Street, Keighley, BD21 1AA', folder: 'alhidaayah', tags: 'Bradford Keighley' },
    { name: 'Al-Mustaqeem Education and Community Centre', addr: '4 Central Avenue, Bradford, BD5 0PB', folder: 'almustaqeem', tags: 'Bradford' },
    { name: 'Azharul Madaaris', addr: '102 Princeville Road, Lidget Green, Bradford, BD7 2AR', folder: 'azharulmadaaris', tags: 'Bradford Lidget Green Great Horton' },
    { name: 'Madrasah Baitul Ilm', addr: '4 St Johns Court, Square Street, Bradford, BD4 7NP', folder: 'baitulilm', tags: 'Bradford' },
    { name: 'Darul Mahmood', addr: '21 St. Mary's Road, Bradford, BD8 7LR', folder: 'darulmahmood', tags: 'Bradford' },
    { name: 'Doha Mosque (مسجد الدوحة)', addr: '13-15 Claremont, Bradford, BD7 1BG', folder: 'doha', tags: 'Bradford Great Horton' },
    { name: 'Firdaws Islamic Centre / Firdaws Mosque', addr: 'Males: Guy Street; Females: 75 Edward Street, Bradford, BD4 7BB', folder: 'firdaws', tags: 'Bradford' },
    { name: 'Iqra Masjid', addr: 'Off Farriers Croft, King's Road, Bradford, BD2 1ET', folder: 'iqra', tags: 'Bradford Idle' },
    { name: 'Jamia Abu Hanifa Madrassa', addr: '35 Hustler Street, Undercliffe, BD3 0PS', folder: 'abuhanifa', tags: 'Bradford Undercliffe' },
    { name: 'Jamiah Farooqiah', addr: '432 Barkerend Road, Bradford, BD3 8QJ', folder: 'farooqiah', tags: 'Bradford' },
    { name: 'Madni Masjid (West Bowling Islamic Society)', addr: '133 Newton Street, BD5 7BJ', folder: 'madnimasjid', tags: 'Bradford' },
    { name: 'Madrasa Abbasiya', addr: '1D Moor Park Drive, Bradford, BD3 7ER', folder: 'abbasiya', tags: 'Bradford' },
    { name: 'Markazi Masjid Darul Irfan', addr: '1 Little Cross St, BD5 8AD', folder: 'darulirfan', tags: 'Bradford' },
    { name: 'Masjid Abdullah-bin-Masood (R.A.)', addr: '14 Lynthorne Road, Frizinghall, Bradford', folder: 'abdullahbinmasood', tags: 'Bradford Frizinghall' },
    { name: 'Masjid Ali', addr: '228 Parkside Road, Bradford, BD5 8PW', folder: 'masjidali', tags: 'Bradford' },
    { name: 'Masjid Ayesha', addr: '2 Thornacre Road, Manningham, BD18 1JY', folder: 'masjidayesha', tags: 'Bradford Manningham' },
    { name: 'Masjid Bilal', addr: '1-3 Drummond Rd, Bradford, BD8 8DA', folder: 'masjidbilal', tags: 'Bradford' },
    { name: 'Masjid Hamza', addr: '42 Woodview Terrace, BD8 7AH', folder: 'masjidhamza', tags: 'Bradford' },
    { name: 'Masjid Husain', addr: '203 Allerton Road, BD15 7RD', folder: 'masjidhusain', tags: 'Bradford' },
    { name: 'Masjid Ibraheem & Education Centre', addr: 'Lower Rushton Road, Bradford, BD3 8PX', folder: 'ibraheem', tags: 'Bradford' },
    { name: 'Masjid Namirah / Madrasah Ta'limul Quran', addr: '8-10 Hanover Square, Bradford, West Yorkshire, BD1 3BY', folder: 'namirah', tags: 'Bradford' },
    { name: 'Masjid Noor', addr: '62 Toller Lane, Bradford, West Yorkshire, BD8 9DA', folder: 'masjidnoor', tags: 'Bradford' },
    { name: 'Masjid Noorul Islam', addr: '58-62 St Margaret's Road, Bradford, BD7 3AE', folder: 'noorulislam', tags: 'Bradford Great Horton' },
    { name: 'Nusrat-ul-Islam Masjid', addr: 'Preston Street, Bradford, BD7 1DD', folder: 'nusratul', tags: 'Bradford Great Horton' },
    { name: 'Khanqah Naqshbandia Masjid Farooqia', addr: '28 Gondal Court, Bradford, BD5 9JW', folder: 'farooqia', tags: 'Bradford' },
    { name: 'Masjid-e-Umar', addr: '184 Durham Road, Bradford, BD8 9HU', folder: 'masjidumar', tags: 'Bradford' },
    { name: 'Masjid ~ E ~ Usman / Madrassa Khaliliya', addr: '57 Upper Seymour St, Bradford, BD3 9LJ', folder: 'masjidusman', tags: 'Bradford' },
    { name: 'Masjidur Raashideen', addr: '14 Farfield Street, Bradford, BD9 5AS', folder: 'raashideen', tags: 'Bradford' },
    { name: 'Musalla Salaam', addr: '191 Pasture Lane, Clayton, Bradford, BD7 2SQ', folder: 'musallasalaam', tags: 'Bradford Clayton Great Horton' },
    { name: 'PYC Masjid Ahle Bayt', addr: 'Mount Street, Bradford, BD3 9SR', folder: 'ahlebayt', tags: 'Bradford' },
    { name: 'Shipley Islamic & Education Centre -Jam-e-Masjid- (S.I.E.C)', addr: 'Aireville Road, Bradford, West Yorkshire, BD9 4HH', folder: 'shipley', tags: 'Bradford' },
    { name: 'Wibsey & Buttershaw Islamic Learning Centre / Dawah Centre', addr: 'The Cooperville Centre, Bellerby Brow, Bradford, BD6 3JY', folder: 'wibseybuttershaw', tags: 'Bradford' },
    { name: 'Wibsey Musalla', addr: '75 Odsal Road, Wibsey, BD6 1PN', folder: 'wibsey', tags: 'Bradford Wibsey' },
];

(function() {
    // Detect current mosque from URL
    const path = window.location.pathname;
    const currentFolder = MASJIDS.find(m => path.includes('/' + m.folder + '/'));
    const isHome = !currentFolder;
    const pathPrefix = isHome ? '' : '../';

    // --- Favourites helpers ---
    function getFavs() {
        try { return JSON.parse(localStorage.getItem('waqt-favorites') || '[]'); } catch(e) { return []; }
    }
    function setFavs(favs) { localStorage.setItem('waqt-favorites', JSON.stringify(favs)); }
    function isFav(folder) { return getFavs().indexOf(folder) > -1; }
    function toggleFav(folder, e) {
        if (e) { e.stopPropagation(); e.preventDefault(); }
        var favs = getFavs();
        var idx = favs.indexOf(folder);
        if (idx > -1) favs.splice(idx, 1); else favs.push(folder);
        setFavs(favs);
        updateAllStars();
        updateFavsDropdown();
        updateFavCount();
    }

    // Inject CSS
    const style = document.createElement('style');
    style.textContent = `
        .masjid-nav {
            display: flex; align-items: center; justify-content: space-between;
            background: #1a1a2e; padding: 6px 12px; font-size: 12px;
        }
        .masjid-nav .nav-left { display: flex; align-items: center; gap: 8px; }
        .masjid-nav .nav-right { display: flex; align-items: center; position: relative; }
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
        .nav-list li { display: flex; align-items: center; }
        .nav-list a {
            display: flex; flex-direction: column; padding: 10px 14px;
            color: rgba(255,255,255,0.7); text-decoration: none;
            transition: all 0.15s ease; border-left: 3px solid transparent;
            flex: 1; min-width: 0;
        }
        .nav-list a:hover { background: rgba(255,255,255,0.08); color: white; }
        .nav-list a.active {
            color: white; background: rgba(255,255,255,0.06);
            border-left-color: currentColor; font-weight: 600;
        }
        .nav-list .nav-name { font-size: 13px; }
        .nav-list .nav-addr { font-size: 10px; opacity: 0.45; margin-top: 1px; }
        .nav-list .nav-tags { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
        .nav-item-star {
            color: rgba(255,255,255,0.15); cursor: pointer; font-size: 16px;
            padding: 8px 10px; transition: all 0.15s ease; flex-shrink: 0;
            user-select: none;
        }
        .nav-item-star:hover { color: rgba(255,255,255,0.4); }
        .nav-item-star.active { color: #ffc107; }
        .nav-fav-star {
            color: rgba(255,255,255,0.3); cursor: pointer; font-size: 18px;
            transition: all 0.2s ease; user-select: none; line-height: 1;
        }
        .nav-fav-star:hover { color: rgba(255,255,255,0.6); }
        .nav-fav-star.active { color: #ffc107; }
        .nav-favs-btn {
            display: flex; align-items: center; gap: 5px;
            color: rgba(255,255,255,0.4); cursor: pointer; font-size: 12px;
            padding: 5px 10px; border-radius: 6px;
            background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.2s ease; user-select: none;
        }
        .nav-favs-btn:hover { background: rgba(255,255,255,0.15); color: white; }
        .nav-favs-btn .fav-icon { font-size: 14px; color: #ffc107; }
        .nav-favs-btn .fav-count {
            background: #ffc107; color: #1a1a2e; font-size: 9px; font-weight: 700;
            border-radius: 50%; min-width: 16px; height: 16px;
            display: flex; align-items: center; justify-content: center; padding: 0 4px;
        }
        .nav-favs-dropdown {
            display: none; position: absolute; top: calc(100% + 6px); right: 0;
            background: #1a1a2e; border: 1px solid rgba(255,255,255,0.15);
            border-radius: 8px; min-width: 260px; max-height: 320px;
            overflow-y: auto; z-index: 201; box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        }
        .nav-favs-dropdown.open { display: block; }
        .nav-favs-label {
            padding: 10px 14px 6px; font-size: 10px; text-transform: uppercase;
            letter-spacing: 1px; color: rgba(255,255,255,0.3);
        }
        .nav-favs-empty {
            padding: 20px 16px; text-align: center; color: rgba(255,255,255,0.25);
            font-size: 12px; line-height: 1.6;
        }
        .nav-all {
            display: block; text-align: center; padding: 8px;
            color: rgba(255,255,255,0.4); text-decoration: none;
            font-size: 11px; border-top: 1px solid rgba(255,255,255,0.08);
            transition: all 0.15s ease;
        }
        .nav-all:hover { color: white; background: rgba(255,255,255,0.05); }
        body.dark-mode .masjid-nav { background: #111122; }
        body.dark-mode .nav-dropdown { background: #111122; }
        body.dark-mode .nav-favs-dropdown { background: #111122; }
        @media print { .masjid-nav, .nav-dropdown, .nav-favs-dropdown { display: none !important; } }
    `;
    document.head.appendChild(style);

    // Build nav HTML — dropdown items with star toggles
    var items = MASJIDS.map(function(m) {
        var isActive = currentFolder && m.folder === currentFolder.folder;
        var starred = isFav(m.folder);
        return '<li><a href="' + pathPrefix + m.folder + '/"' + (isActive ? ' class="active"' : '') + '><span class="nav-name">' + m.name + '</span><span class="nav-addr">' + m.addr + '</span>' + (m.tags ? '<span class="nav-tags">' + m.tags + '</span>' : '') + '</a><span class="nav-item-star' + (starred ? ' active' : '') + '" data-folder="' + m.folder + '" title="Toggle favourite">&#9733;</span></li>';
    }).join('');

    var initFavs = getFavs();
    var nav = document.createElement('nav');
    nav.className = 'masjid-nav';
    nav.innerHTML =
        '<div class="nav-left">' +
            '<span class="nav-label">Masjid</span>' +
            '<div class="nav-selector">' +
                '<div class="nav-current" id="navToggle">' + (currentFolder ? currentFolder.name : 'Select Masjid') + '</div>' +
                '<div class="nav-dropdown" id="navDropdown">' +
                    '<input type="text" class="nav-search" id="navSearch" placeholder="Search masjids...">' +
                    '<ul class="nav-list" id="navList">' + items + '</ul>' +
                    (isHome ? '' : '<a href="../" class="nav-all">View all masjids</a>') +
                '</div>' +
            '</div>' +
            (!isHome && currentFolder ? '<span class="nav-fav-star' + (isFav(currentFolder.folder) ? ' active' : '') + '" id="navFavStar" title="' + (isFav(currentFolder.folder) ? 'Remove from' : 'Add to') + ' favourites">&#9733;</span>' : '') +
        '</div>' +
        '<div class="nav-right">' +
            '<div class="nav-favs-btn" id="navFavsBtn">' +
                '<span class="fav-icon">&#9733;</span>' +
                '<span class="fav-count" id="navFavCount"' + (initFavs.length ? '' : ' style="display:none;"') + '>' + initFavs.length + '</span>' +
            '</div>' +
            '<div class="nav-favs-dropdown" id="navFavsDropdown">' +
                '<div class="nav-favs-label">Favourites</div>' +
                '<ul class="nav-list" id="navFavsList"></ul>' +
                '<div class="nav-favs-empty" id="navFavsEmpty">No favourites yet</div>' +
            '</div>' +
        '</div>';

    // Insert nav as first child of .container
    var container = document.querySelector('.container');
    if (container) container.insertBefore(nav, container.firstChild);

    // --- Favourites UI updates ---
    function updateFavsDropdown() {
        var favs = getFavs();
        var list = document.getElementById('navFavsList');
        var empty = document.getElementById('navFavsEmpty');
        if (!list) return;
        if (favs.length === 0) {
            list.innerHTML = '';
            if (empty) empty.style.display = '';
            return;
        }
        if (empty) empty.style.display = 'none';
        list.innerHTML = favs.map(function(folder) {
            var m = MASJIDS.find(function(x) { return x.folder === folder; });
            if (!m) return '';
            var isActive = currentFolder && m.folder === currentFolder.folder;
            return '<li><a href="' + pathPrefix + m.folder + '/"' + (isActive ? ' class="active"' : '') + '><span class="nav-name">' + m.name + '</span><span class="nav-addr">' + m.addr + '</span></a><span class="nav-item-star active" data-folder="' + m.folder + '" title="Remove from favourites">&#9733;</span></li>';
        }).join('');
        list.querySelectorAll('.nav-item-star').forEach(function(star) {
            star.addEventListener('click', function(e) { toggleFav(this.getAttribute('data-folder'), e); });
        });
    }

    function updateAllStars() {
        document.querySelectorAll('#navList .nav-item-star').forEach(function(star) {
            var folder = star.getAttribute('data-folder');
            if (isFav(folder)) star.classList.add('active'); else star.classList.remove('active');
        });
        var navStar = document.getElementById('navFavStar');
        if (navStar && currentFolder) {
            if (isFav(currentFolder.folder)) { navStar.classList.add('active'); navStar.title = 'Remove from favourites'; }
            else { navStar.classList.remove('active'); navStar.title = 'Add to favourites'; }
        }
    }

    function updateFavCount() {
        var count = getFavs().length;
        var el = document.getElementById('navFavCount');
        if (el) { el.textContent = count; el.style.display = count ? '' : 'none'; }
    }

    // Initialize favourites dropdown
    updateFavsDropdown();

    // --- Event handlers ---

    // Main dropdown toggle
    document.getElementById('navToggle').addEventListener('click', function() {
        var dd = document.getElementById('navDropdown');
        dd.classList.toggle('open');
        var fd = document.getElementById('navFavsDropdown');
        if (fd) fd.classList.remove('open');
        if (dd.classList.contains('open')) {
            var search = document.getElementById('navSearch');
            search.value = '';
            filterNav();
            setTimeout(function() { search.focus(); }, 50);
        }
    });

    document.getElementById('navSearch').addEventListener('input', filterNav);

    function filterNav() {
        var q = document.getElementById('navSearch').value.toLowerCase();
        document.querySelectorAll('#navList li').forEach(function(li) {
            li.style.display = li.textContent.toLowerCase().includes(q) ? '' : 'none';
        });
    }

    // Star handlers in main dropdown
    document.querySelectorAll('#navList .nav-item-star').forEach(function(star) {
        star.addEventListener('click', function(e) { toggleFav(this.getAttribute('data-folder'), e); });
    });

    // Nav bar star (current mosque favourite toggle)
    var navFavStar = document.getElementById('navFavStar');
    if (navFavStar && currentFolder) {
        navFavStar.addEventListener('click', function() { toggleFav(currentFolder.folder); });
    }

    // Favourites button toggle
    var favsBtn = document.getElementById('navFavsBtn');
    if (favsBtn) {
        favsBtn.addEventListener('click', function() {
            var fd = document.getElementById('navFavsDropdown');
            fd.classList.toggle('open');
            var dd = document.getElementById('navDropdown');
            if (dd) dd.classList.remove('open');
            if (fd.classList.contains('open')) updateFavsDropdown();
        });
    }

    // Close dropdowns on outside click
    document.addEventListener('click', function(e) {
        var dd = document.getElementById('navDropdown');
        if (dd && !e.target.closest('.nav-selector')) dd.classList.remove('open');
        var fd = document.getElementById('navFavsDropdown');
        if (fd && !e.target.closest('.nav-right')) fd.classList.remove('open');
    });
})();
