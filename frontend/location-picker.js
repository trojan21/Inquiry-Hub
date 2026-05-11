/**
 * location-picker.js — Shared India State + City dropdown
 * ─────────────────────────────────────────────────────────
 * Usage:
 *   window.initLocationPicker({
 *     stateTriggerId:    'state-trigger',
 *     stateValueId:      'state-value',
 *     stateDropId:       'state-drop',
 *     stateSearchId:     'state-search',
 *     stateListId:       'state-list',
 *     stateOfflineBadge: 'state-offline-badge',
 *     cityTriggerId:     'city-trigger',
 *     cityValueId:       'city-value',
 *     cityDropId:        'city-drop',
 *     citySearchId:      'city-search',
 *     cityListId:        'city-list',
 *     cityOfflineBadge:  'city-offline-badge',
 *     cityHiddenId:      'city-hidden',
 *     wrapperSelector:   '#loc-wrapper',   // for click-outside
 *     namespace:         'loc',            // prefix for window fns to avoid collision
 *     onCityPicked:      (city) => {},     // optional callback
 *   })
 *
 * Returns a controller: { reset(), getCity(), getState() }
 */

(function (global) {

  /* ── FALLBACK — major Indian states + cities ──────────── */
  const FALLBACK = {
    states: [
      {name:"Andaman and Nicobar",    isoCode:"AN"},{name:"Andhra Pradesh",         isoCode:"AP"},
      {name:"Arunachal Pradesh",      isoCode:"AR"},{name:"Assam",                  isoCode:"AS"},
      {name:"Bihar",                  isoCode:"BR"},{name:"Chandigarh",             isoCode:"CH"},
      {name:"Chhattisgarh",           isoCode:"CG"},{name:"Dadra and Nagar Haveli", isoCode:"DN"},
      {name:"Daman and Diu",          isoCode:"DD"},{name:"Delhi",                  isoCode:"DL"},
      {name:"Goa",                    isoCode:"GA"},{name:"Gujarat",                isoCode:"GJ"},
      {name:"Haryana",                isoCode:"HR"},{name:"Himachal Pradesh",       isoCode:"HP"},
      {name:"Jammu and Kashmir",      isoCode:"JK"},{name:"Jharkhand",              isoCode:"JH"},
      {name:"Karnataka",              isoCode:"KA"},{name:"Kerala",                 isoCode:"KL"},
      {name:"Ladakh",                 isoCode:"LA"},{name:"Lakshadweep",            isoCode:"LD"},
      {name:"Madhya Pradesh",         isoCode:"MP"},{name:"Maharashtra",            isoCode:"MH"},
      {name:"Manipur",                isoCode:"MN"},{name:"Meghalaya",              isoCode:"ML"},
      {name:"Mizoram",                isoCode:"MZ"},{name:"Nagaland",               isoCode:"NL"},
      {name:"Odisha",                 isoCode:"OR"},{name:"Puducherry",             isoCode:"PY"},
      {name:"Punjab",                 isoCode:"PB"},{name:"Rajasthan",              isoCode:"RJ"},
      {name:"Sikkim",                 isoCode:"SK"},{name:"Tamil Nadu",             isoCode:"TN"},
      {name:"Telangana",              isoCode:"TG"},{name:"Tripura",                isoCode:"TR"},
      {name:"Uttar Pradesh",          isoCode:"UP"},{name:"Uttarakhand",            isoCode:"UT"},
      {name:"West Bengal",            isoCode:"WB"},
    ],
    cities: {
      AN:["Port Blair","Diglipur","Mayabunder","Car Nicobar"],
      AP:["Visakhapatnam","Vijayawada","Guntur","Nellore","Kurnool","Kakinada","Tirupati","Rajahmundry","Kadapa","Anantapur","Vizianagaram","Eluru"],
      AR:["Itanagar","Naharlagun","Pasighat","Tawang","Ziro","Bomdila"],
      AS:["Guwahati","Silchar","Dibrugarh","Jorhat","Nagaon","Tinsukia","Tezpur","Bongaigaon","Dhubri","Goalpara","Lakhimpur","Karimganj"],
      BR:["Patna","Gaya","Bhagalpur","Muzaffarpur","Darbhanga","Purnia","Ara","Bihar Sharif","Begusarai","Katihar","Munger","Chapra","Hajipur","Samastipur"],
      CH:["Chandigarh"],
      CG:["Raipur","Bhilai","Bilaspur","Korba","Durg","Rajnandgaon","Jagdalpur","Ambikapur","Raigarh","Chirmiri","Dhamtari","Mahasamund"],
      DN:["Silvassa","Amli","Dadra"],
      DD:["Daman","Diu"],
      DL:["New Delhi","Dwarka","Rohini","Saket","Karol Bagh","Lajpat Nagar","Janakpuri","Pitampura","Shahdara","Vasant Kunj","Mayur Vihar","Preet Vihar"],
      GA:["Panaji","Margao","Vasco da Gama","Mapusa","Ponda","Bicholim","Valpoi","Sanquelim","Canacona","Pernem"],
      GJ:["Ahmedabad","Surat","Vadodara","Rajkot","Bhavnagar","Jamnagar","Junagadh","Gandhinagar","Anand","Mehsana","Morbi","Nadiad","Bharuch","Navsari","Amreli","Botad"],
      HR:["Gurugram","Faridabad","Panipat","Ambala","Yamunanagar","Rohtak","Hisar","Karnal","Sonipat","Panchkula","Rewari","Bhiwani","Sirsa","Bahadurgarh"],
      HP:["Shimla","Dharamshala","Solan","Mandi","Kullu","Hamirpur","Bilaspur","Chamba","Una","Nahan","Palampur","Baddi"],
      JK:["Srinagar","Jammu","Anantnag","Sopore","Baramulla","Kathua","Udhampur","Punch","Rajouri","Leh"],
      JH:["Ranchi","Jamshedpur","Dhanbad","Bokaro","Deoghar","Hazaribagh","Giridih","Ramgarh","Medininagar","Chaibasa","Dumka","Phusro"],
      KA:["Bengaluru","Mysuru","Hubli","Mangaluru","Belagavi","Kalaburagi","Davanagere","Ballari","Vijayapura","Shivamogga","Tumakuru","Bidar","Udupi","Mandya","Hassan","Raichur"],
      KL:["Thiruvananthapuram","Kochi","Kozhikode","Thrissur","Kollam","Palakkad","Alappuzha","Malappuram","Kannur","Kottayam","Pathanamthitta","Idukki","Kasaragod","Wayanad"],
      LA:["Leh","Kargil"],
      LD:["Kavaratti","Agatti","Minicoy"],
      MP:["Bhopal","Indore","Jabalpur","Gwalior","Ujjain","Sagar","Dewas","Satna","Ratlam","Rewa","Murwara","Singrauli","Chhindwara","Burhanpur","Khandwa"],
      MH:["Mumbai","Pune","Nagpur","Thane","Nashik","Aurangabad","Solapur","Kolhapur","Amravati","Nanded","Sangli","Jalgaon","Akola","Latur","Dhule","Ahmednagar","Chandrapur","Parbhani"],
      MN:["Imphal","Thoubal","Kakching","Senapati","Churachandpur","Bishnupur"],
      ML:["Shillong","Tura","Jowai","Nongstoin","Williamnagar"],
      MZ:["Aizawl","Lunglei","Saiha","Champhai","Kolasib"],
      NL:["Kohima","Dimapur","Mokokchung","Tuensang","Wokha","Zunheboto"],
      OR:["Bhubaneswar","Cuttack","Rourkela","Brahmapur","Sambalpur","Puri","Balasore","Bhadrak","Baripada","Jharsuguda","Angul","Dhenkanal","Koraput","Kendujhar"],
      PY:["Puducherry","Karaikal","Mahe","Yanam"],
      PB:["Ludhiana","Amritsar","Jalandhar","Patiala","Bathinda","Mohali","Firozpur","Hoshiarpur","Gurdaspur","Moga","Pathankot","Sangrur","Barnala","Fatehgarh Sahib"],
      RJ:["Jaipur","Jodhpur","Kota","Bikaner","Ajmer","Udaipur","Bhilwara","Alwar","Bharatpur","Sikar","Pali","Sri Ganganagar","Barmer","Churu","Jhunjhunu","Nagaur","Tonk"],
      SK:["Gangtok","Namchi","Gyalshing","Mangan","Rangpo"],
      TN:["Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem","Tirunelveli","Tiruppur","Erode","Vellore","Thoothukudi","Dindigul","Thanjavur","Kanchipuram","Nagercoil","Kumbakonam","Hosur"],
      TG:["Hyderabad","Warangal","Nizamabad","Karimnagar","Khammam","Ramagundam","Secunderabad","Mahbubnagar","Nalgonda","Adilabad","Suryapet","Siddipet"],
      TR:["Agartala","Dharmanagar","Udaipur","Kailasahar","Belonia","Ambassa"],
      UP:["Lucknow","Kanpur","Agra","Varanasi","Meerut","Allahabad (Prayagraj)","Ghaziabad","Noida","Bareilly","Aligarh","Moradabad","Saharanpur","Gorakhpur","Firozabad","Mathura","Muzaffarnagar","Shahjahanpur","Jhansi","Rampur","Hapur"],
      UT:["Dehradun","Haridwar","Roorkee","Haldwani","Rudrapur","Kashipur","Rishikesh","Pithoragarh","Almora","Mussoorie","Kotdwar","Ramnagar"],
      WB:["Kolkata","Asansol","Siliguri","Durgapur","Bardhaman","Malda","Baharampur","Habra","Kharagpur","Shantipur","Jalpaiguri","Haldia","Darjeeling","Cooch Behar","Krishnanagar","Raiganj"],
    }
  };

  const CDN_BASE    = 'https://cdn.jsdelivr.net/npm/country-state-city@3.2.1/dist/lib';
  const CDN_TIMEOUT = 5000;

  function fetchWithTimeout(url, ms) {
    return new Promise((resolve, reject) => {
      const id = setTimeout(() => reject(new Error('timeout')), ms);
      fetch(url).then(r => { clearTimeout(id); resolve(r); })
                .catch(e => { clearTimeout(id); reject(e); });
    });
  }

  /* ── CDN data — loaded once, shared across all instances ── */
  let _cdnStates         = null;
  let _cdnCitiesByState  = null;
  let _cdnLoading        = null;   // promise

  function loadCDN() {
    if (_cdnLoading) return _cdnLoading;
    _cdnLoading = (async () => {
      const [statesRes, citiesRes] = await Promise.all([
        fetchWithTimeout(`${CDN_BASE}/state.json`, CDN_TIMEOUT),
        fetchWithTimeout(`${CDN_BASE}/city.json`,  CDN_TIMEOUT),
      ]);
      const allStates = await statesRes.json();
      const allCities = await citiesRes.json();

      _cdnStates = allStates
        .filter(s => s.countryCode === 'IN')
        .sort((a, b) => a.name.localeCompare(b.name));

      _cdnCitiesByState = {};
      allCities.forEach(c => {
        const name        = Array.isArray(c) ? c[0] : c.name;
        const stateCode   = Array.isArray(c) ? c[1] : c.stateCode;
        const countryCode = Array.isArray(c) ? c[2] : c.countryCode;
        if (countryCode !== 'IN') return;
        if (!_cdnCitiesByState[stateCode]) _cdnCitiesByState[stateCode] = [];
        _cdnCitiesByState[stateCode].push(name);
      });
    })();
    return _cdnLoading;
  }

  /* ── Factory ─────────────────────────────────────────── */
  function initLocationPicker(cfg) {
    const ns = cfg.namespace || 'loc';

    // per-instance state
    const st = {
      states: [], cities: [],
      selectedState: null, selectedCity: null,
      openDrop: null, _citiesByState: {}, usingFallback: false,
    };

    // helper — get element safely
    const el = id => document.getElementById(id);

    function esc(s) { return s.replace(/\\/g, '\\\\').replace(/'/g, "\\'"); }

    /* ── Render helpers ─────────────────────────────── */
    function stateItem(s) {
      const active = st.selectedState?.isoCode === s.isoCode ? ' class="active"' : '';
      return `<li${active} onclick="window['_${ns}PickState']('${esc(s.isoCode)}','${esc(s.name)}')">${s.name}</li>`;
    }
    function cityItem(name) {
      const active = st.selectedCity === name ? ' class="active"' : '';
      return `<li${active} onclick="window['_${ns}PickCity']('${esc(name)}')">${name}</li>`;
    }
    function renderStateList() {
      const list = el(cfg.stateListId);
      if (!list) return;
      list.innerHTML = st.states.length
        ? st.states.map(s => stateItem(s)).join('')
        : '<li class="loc-empty">No states found</li>';
    }

    /* ── Open / close ───────────────────────────────── */
    function openDrop(which) {
      st.openDrop = which;
      const dropId    = which === 'state' ? cfg.stateDropId    : cfg.cityDropId;
      const triggerId = which === 'state' ? cfg.stateTriggerId : cfg.cityTriggerId;
      const searchId  = which === 'state' ? cfg.stateSearchId  : cfg.citySearchId;
      el(dropId)?.classList.add('open');
      el(triggerId)?.classList.add('open');
      setTimeout(() => el(searchId)?.focus(), 50);
    }
    function closeDrop(which) {
      if (st.openDrop === which) st.openDrop = null;
      const dropId    = which === 'state' ? cfg.stateDropId    : cfg.cityDropId;
      const triggerId = which === 'state' ? cfg.stateTriggerId : cfg.cityTriggerId;
      const searchId  = which === 'state' ? cfg.stateSearchId  : cfg.citySearchId;
      el(dropId)?.classList.remove('open');
      el(triggerId)?.classList.remove('open');
      const s = el(searchId);
      if (s && s.value) { s.value = ''; filterList(which); }
    }

    /* ── Global toggle (called from HTML onclick) ───── */
    window[`_${ns}Toggle`] = function (which) {
      if (st.openDrop === which) { closeDrop(which); return; }
      if (st.openDrop) closeDrop(st.openDrop);
      openDrop(which);
    };

    /* ── Pick state ─────────────────────────────────── */
    window[`_${ns}PickState`] = function (isoCode, name) {
      st.selectedState = { isoCode, name };
      st.selectedCity  = null;

      const sv = el(cfg.stateValueId);
      if (sv) sv.textContent = name;
      el(cfg.stateTriggerId)?.classList.add('selected');
      el(cfg.stateTriggerId)?.classList.remove('invalid');

      const cities = (st._citiesByState[isoCode] || []).slice().sort();
      st.cities = cities;

      el(cfg.cityOfflineBadge)?.classList.toggle('visible', st.usingFallback);
      const cs = el(cfg.citySearchId);
      if (cs) cs.value = '';
      const cl = el(cfg.cityListId);
      if (cl) cl.innerHTML = cities.length
        ? cities.map(c => cityItem(c)).join('')
        : '<li class="loc-empty">No cities found for this state</li>';

      const cv = el(cfg.cityValueId);
      if (cv) cv.textContent = 'Select City';
      const ch = el(cfg.cityHiddenId);
      if (ch) ch.value = '';

      const ct = el(cfg.cityTriggerId);
      ct?.classList.remove('selected', 'disabled', 'invalid');

      el(cfg.stateListId)?.querySelectorAll('li').forEach(li => {
        li.classList.toggle('active', li.textContent.trim() === name);
      });

      closeDrop('state');
      setTimeout(() => openDrop('city'), 180);
    };

    /* ── Pick city ──────────────────────────────────── */
    window[`_${ns}PickCity`] = function (name) {
      st.selectedCity = name;
      const cv = el(cfg.cityValueId);
      if (cv) cv.textContent = name;
      const ch = el(cfg.cityHiddenId);
      if (ch) ch.value = name;
      el(cfg.cityTriggerId)?.classList.add('selected');
      el(cfg.cityTriggerId)?.classList.remove('invalid');
      el(cfg.cityListId)?.querySelectorAll('li').forEach(li => {
        li.classList.toggle('active', li.textContent.trim() === name);
      });
      closeDrop('city');
      if (cfg.onCityPicked) cfg.onCityPicked(name);
    };

    /* ── Filter search — case-insensitive, word-start priority, highlight ── */
    function highlight(text, q) {
      if (!q) return text;
      const idx = text.toLowerCase().indexOf(q.toLowerCase());
      if (idx === -1) return text;
      return text.slice(0, idx)
        + `<mark style="background:rgba(37,99,235,.12);color:#2563eb;border-radius:3px;padding:0 2px;">">`
        + text.slice(idx, idx + q.length)
        + `</mark>`
        + text.slice(idx + q.length);
    }

    function sortByRelevance(items, getName, q) {
      // word-start matches first, then contains
      const ql = q.toLowerCase();
      return [...items].sort((a, b) => {
        const an = getName(a).toLowerCase();
        const bn = getName(b).toLowerCase();
        const aStart = an.startsWith(ql) || an.split(' ').some(w => w.startsWith(ql));
        const bStart = bn.startsWith(ql) || bn.split(' ').some(w => w.startsWith(ql));
        if (aStart && !bStart) return -1;
        if (!aStart && bStart) return 1;
        return an.localeCompare(bn);
      });
    }

    function filterList(which) {
      const searchId = which === 'state' ? cfg.stateSearchId : cfg.citySearchId;
      const listId   = which === 'state' ? cfg.stateListId   : cfg.cityListId;
      const q   = (el(searchId)?.value || '').trim();
      const ql  = q.toLowerCase();
      const list = el(listId);
      if (!list) return;

      if (which === 'state') {
        const filtered = ql
          ? sortByRelevance(
              st.states.filter(s => s.name.toLowerCase().includes(ql)),
              s => s.name, ql
            )
          : st.states;
        list.innerHTML = filtered.length
          ? filtered.map(s => {
              const active = st.selectedState?.isoCode === s.isoCode ? ' class="active"' : '';
              return `<li${active} onclick="window['_${ns}PickState']('${esc(s.isoCode)}','${esc(s.name)}')">${highlight(s.name, q)}</li>`;
            }).join('')
          : '<li class="loc-empty">No match found</li>';
      } else {
        const filtered = ql
          ? sortByRelevance(
              st.cities.filter(c => c.toLowerCase().includes(ql)),
              c => c, ql
            )
          : st.cities;
        list.innerHTML = filtered.length
          ? filtered.map(c => {
              const active = st.selectedCity === c ? ' class="active"' : '';
              return `<li${active} onclick="window['_${ns}PickCity']('${esc(c)}')">${highlight(c, q)}</li>`;
            }).join('')
          : '<li class="loc-empty">No match found</li>';
      }
    }
    // expose for oninput= in HTML
    window[`_${ns}FilterList`] = filterList;

    /* ── Reset ──────────────────────────────────────── */
    function reset() {
      st.selectedState = null; st.selectedCity = null;
      if (st.openDrop) closeDrop(st.openDrop);
      const sv = el(cfg.stateValueId); if (sv) sv.textContent = 'Select State';
      const cv = el(cfg.cityValueId);  if (cv) cv.textContent  = 'Select City';
      const ch = el(cfg.cityHiddenId); if (ch) ch.value = '';
      el(cfg.stateTriggerId)?.classList.remove('selected','open','invalid');
      el(cfg.cityTriggerId)?.classList.remove('selected','open','invalid');
      el(cfg.cityTriggerId)?.classList.add('disabled');
      renderStateList();
      const cl = el(cfg.cityListId);
      if (cl) cl.innerHTML = '<li class="loc-placeholder">← Choose a state first</li>';
    }
    window[`_${ns}Reset`] = reset;

    /* ── Click outside ──────────────────────────────── */
    document.addEventListener('click', e => {
      if (cfg.wrapperSelector && !e.target.closest(cfg.wrapperSelector) && st.openDrop) {
        closeDrop(st.openDrop);
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && st.openDrop) closeDrop(st.openDrop);
    });

    /* ── Boot ───────────────────────────────────────── */
    async function init() {
      const stateList = el(cfg.stateListId);
      if (stateList) stateList.innerHTML = '<li class="loc-loading">Loading states…</li>';

      try {
        await loadCDN();
        st.states         = _cdnStates;
        st._citiesByState = _cdnCitiesByState;
        st.usingFallback  = false;
      } catch (err) {
        console.warn('[LocationPicker] CDN unavailable, offline fallback active.', err?.message);
        st.states         = FALLBACK.states;
        st._citiesByState = FALLBACK.cities;
        st.usingFallback  = true;
        el(cfg.stateOfflineBadge)?.classList.add('visible');
      }
      renderStateList();
    }

    init();

    /* ── Public API ─────────────────────────────────── */
    return {
      reset,
      getCity:  () => st.selectedCity,
      getState: () => st.selectedState,
    };
  }

  global.initLocationPicker = initLocationPicker;

})(window);