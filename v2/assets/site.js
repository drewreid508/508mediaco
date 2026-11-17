/* 508 Media Co. — redesign preview behaviour.
   Small on purpose: menu, header border, filters, hover video, lightbox, forms. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = matchMedia('(hover: hover)').matches;

  /* ---- preview notes toggle (preview only) ---- */
  const notesBtn = $('[data-notes]');
  const setNotes = hide => {
    document.documentElement.classList.toggle('hide-notes', hide);
    if (notesBtn) notesBtn.textContent = hide ? 'Show notes' : 'Hide notes';
    try { localStorage.setItem('508-hide-notes', hide ? '1' : '0'); } catch (e) {}
  };
  try { if (localStorage.getItem('508-hide-notes') === '1') setNotes(true); } catch (e) {}
  notesBtn?.addEventListener('click', () => setNotes(!document.documentElement.classList.contains('hide-notes')));

  /* ---- header ---- */
  const hdr = $('.hdr');
  const onScroll = () => hdr.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const menuBtn = $('.menu-btn');
  menuBtn?.addEventListener('click', () => {
    const open = !document.body.classList.contains('menu-open');
    document.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', open);
  });
  addEventListener('keydown', e => { if (e.key === 'Escape' && document.body.classList.contains('menu-open')) menuBtn.click(); });

  /* ---- autoplay loops: only while on screen, never on reduced motion ---- */
  const loops = $$('video[data-loop]');
  if (loops.length) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      const v = e.target;
      if (e.isIntersecting && !reduce) { if (!v.src) v.src = v.dataset.loop; v.play().catch(() => {}); }
      else v.pause();
    }), { rootMargin: '120px' });
    loops.forEach(v => io.observe(v));
    document.addEventListener('visibilitychange', () => { if (!document.hidden) loops.forEach(v => { if (v.src && v.getBoundingClientRect().top < innerHeight) v.play().catch(() => {}); }); });
  }

  /* ---- chooser doors: preview clip on hover (desktop only) ---- */
  if (canHover && !reduce) $$('.door[data-preview]').forEach(d => {
    let v;
    d.addEventListener('mouseenter', () => {
      if (!v) { v = document.createElement('video'); v.muted = true; v.loop = true; v.playsInline = true; v.src = d.dataset.preview; v.setAttribute('aria-hidden', 'true'); d.prepend(v); }
      v.play().then(() => d.classList.add('playing')).catch(() => {});
    });
    d.addEventListener('mouseleave', () => { d.classList.remove('playing'); v && v.pause(); });
  });

  /* ---- portfolio filters ---- */
  $$('[data-filter-root]').forEach(root => {
    const grid = $('[data-grid]', root);
    const tiles = $$('.tile', grid);
    const state = { cat: root.dataset.cat || 'all', tag: 'all', kind: 'all' };
    const empty = $('.empty', root);
    const apply = () => {
      let n = 0;
      tiles.forEach(t => {
        const ok = (state.cat === 'all' || t.dataset.cat === state.cat)
          && (state.tag === 'all' || t.dataset.tags.split(' ').includes(state.tag))
          && (state.kind === 'all' || t.dataset.kind === state.kind);
        t.hidden = !ok; if (ok) n++;
      });
      if (empty) empty.hidden = n > 0;
    };
    $$('[data-set]', root).forEach(b => b.addEventListener('click', () => {
      const [k, v] = b.dataset.set.split(':');
      state[k] = v;
      if (k === 'cat') {               // switching tab resets the style chips
        state.tag = 'all';
        $$('[data-tagset]', root).forEach(g => g.hidden = g.dataset.tagset !== v);
        $$('[data-tagset] [data-set]', root).forEach(c => c.setAttribute('aria-pressed', c.dataset.set === 'tag:all'));
        const u = new URL(location); u.searchParams.set('show', v); history.replaceState(null, '', u);
      }
      $$(`[data-set^="${k}:"]`, root).forEach(o => {
        if (o.closest('[role=tablist]')) o.setAttribute('aria-selected', o === b);
        else o.setAttribute('aria-pressed', o.dataset.set === `${k}:${v}`);
      });
      apply();
    }));
    const show = new URLSearchParams(location.search).get('show');
    if (show) $(`[data-set="cat:${show}"]`, root)?.click(); else apply();
  });

  /* ---- lightbox ---- */
  const lb = $('dialog.lb');
  if (lb) {
    const media = $('.lb-media', lb), cap = $('.lb-cap', lb);
    let list = [], i = 0;
    const show = k => {
      i = (k + list.length) % list.length;
      const t = list[i];
      media.innerHTML = '';
      const meta = t.querySelector('.meta');
      const alt = t.querySelector('img').alt;
      if (t.dataset.kind === 'video') {
        const v = document.createElement('video');
        v.src = t.dataset.src; v.controls = true; v.playsInline = true; v.autoplay = true;
        v.poster = t.querySelector('img').src; v.setAttribute('aria-label', alt);
        media.append(v);
      } else {
        const im = document.createElement('img'); im.src = t.dataset.src; im.alt = alt; media.append(im);
      }
      cap.innerHTML = `<b>${meta.children[0].textContent}</b>${meta.children[1].textContent} · ${i + 1} of ${list.length}`;
      const multi = list.length > 1;
      $('.lb-prev', lb).hidden = $('.lb-next', lb).hidden = !multi;
    };
    const close = () => { media.innerHTML = ''; lb.close(); };
    document.addEventListener('click', e => {
      const t = e.target.closest('.tile');
      if (!t) return;
      const grid = t.closest('[data-grid]');
      list = $$('.tile', grid).filter(x => !x.hidden);
      lb.showModal(); show(list.indexOf(t));
    });
    $('.lb-x', lb).onclick = close;
    $('.lb-prev', lb).onclick = () => show(i - 1);
    $('.lb-next', lb).onclick = () => show(i + 1);
    lb.addEventListener('cancel', e => { e.preventDefault(); close(); });
    lb.addEventListener('click', e => { if (e.target.classList.contains('lb-in')) close(); });
    lb.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft' && list.length > 1) show(i - 1);
      if (e.key === 'ArrowRight' && list.length > 1) show(i + 1);
    });
    let x0 = null;
    lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (x0 == null || list.length < 2 || e.target.closest('video')) return;
      const dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
    });
  }

  /* ---- inquiry form ---- */
  const form = $('#inquiry');
  if (form) {
    const qs = new URLSearchParams(location.search);
    const today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
    $$('input[type=date]', form).forEach(d => d.min = today.toISOString().slice(0, 10));

    const setType = t => {
      $$('[data-for]', form).forEach(s => {
        const on = s.dataset.for === t;
        s.hidden = !on;
        $$('input,select,textarea', s).forEach(f => f.disabled = !on);
      });
      $('#form-title').textContent = t === 'auto' ? 'Automotive shoot request' : 'Business project request';
    };
    $$('input[name=kind]', form).forEach(r => r.addEventListener('change', () => setType(r.value)));
    const start = qs.get('type') === 'automotive' ? 'auto' : 'business';
    $(`input[name=kind][value=${start}]`, form).checked = true;
    setType(start);

    // pre-select service / package from links like ?type=business&service=monthly&package=growth
    const svc = qs.get('service'), pkg = qs.get('package');
    if (svc) { const s = $('#b-service'); if ([...s.options].some(o => o.value === svc)) s.value = svc; }
    const pkgRow = $('#b-package-row');
    const syncPkg = () => { const on = $('#b-service').value === 'monthly'; pkgRow.hidden = !on; $('#b-package').disabled = !on; };
    $('#b-service').addEventListener('change', syncPkg);
    if (pkg) $('#b-package').value = pkg;
    syncPkg();

    const fieldOf = el => el.closest('.field');
    const check = el => {
      if (el.disabled) return true;
      const f = fieldOf(el); if (!f) return true;
      let ok = el.checkValidity();
      if (el.type === 'tel' && el.value.trim()) ok = el.value.replace(/\D/g, '').length >= 10;
      f.classList.toggle('err', !ok);
      return ok;
    };
    form.addEventListener('blur', e => { if (e.target.matches('input,select,textarea') && fieldOf(e.target)?.classList.contains('err')) check(e.target); }, true);
    form.addEventListener('input', e => { if (fieldOf(e.target)?.classList.contains('err')) check(e.target); });

    form.addEventListener('submit', e => {
      e.preventDefault();
      const els = $$('input,select,textarea', form).filter(x => !x.disabled && x.name);
      const bad = els.filter(x => !check(x));
      // automotive: at least one coverage type
      const cov = $$('input[name=coverage]', form).filter(c => !c.disabled);
      const covField = $('#a-coverage');
      if (cov.length && !cov.some(c => c.checked)) { covField.classList.add('err'); bad.push(cov[0]); } else covField?.classList.remove('err');
      if (bad.length) { bad[0].focus({ preventScroll: true }); bad[0].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); return; }

      const data = {};
      new FormData(form).forEach((v, k) => { data[k] = data[k] ? `${data[k]}, ${v}` : v; });
      $('#first-name').textContent = (data.name || '').split(' ')[0] || 'there';
      const finish = () => {
        form.classList.remove('sending');
        form.hidden = true; $('#done').hidden = false;
        $('#done').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
        $('#done h2').focus();
      };
      if (!document.documentElement.hasAttribute('data-live')) {
        // PREVIEW build: nothing is sent.
        console.info('[preview] inquiry payload (not sent):', data);
        $('#payload').textContent = Object.entries(data).filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
        return finish();
      }
      // LIVE: same Google Form + Sheet as before (BookingAlerts.gs texts/emails Drew).
      // Never send an empty string: a blank Required question silently drops the whole row.
      const auto = data.kind === 'auto', nz = v => (v && String(v).trim()) || '(not given)';
      const when = (d, t) => d ? `${d}${t ? ' (' + t + ')' : ''}` : '';
      const vehicle = [data.vehicle_year, data.vehicle_make, data.vehicle_model].filter(Boolean).join(' ');
      const lines = ['*** SOURCE: 508 MEDIA CO. (508mediaco.com) ***', '',
        'Type: ' + (auto ? 'Automotive' : 'Business'),
        'Service: ' + nz(data.service)];
      if (!auto && data.package) lines.push('Monthly package: ' + data.package);
      if (auto) lines.push('Vehicle: ' + nz(vehicle), 'Coverage: ' + nz(data.coverage));
      lines.push('Preferred: ' + nz(when(data.preferred_date, data.preferred_time)),
        'Backup: ' + nz(when(data.backup_date, data.backup_time)), '', 'Details:', nz(data.details));
      const body = new URLSearchParams({
        'entry.207022369': nz(data.name),
        'entry.444221534': auto ? nz(vehicle) : nz(data.business),
        'entry.1777192855': nz(data.email),
        'entry.1805905143': nz(data.phone),
        'entry.2066163859': (auto ? 'Automotive: ' : 'Business: ') + nz(data.service) + (data.package ? ' / ' + data.package : ''),
        'entry.111280340': '(not asked)',
        'entry.34369500': nz(when(data.preferred_date, data.preferred_time)),
        'entry.2058135756': nz(data.location),
        'entry.339321494': lines.join('\n'),
      });
      form.classList.add('sending');
      const btn = $('button[type=submit]', form); if (btn) btn.disabled = true;
      fetch('https://docs.google.com/forms/d/e/1FAIpQLSd-G2A4Y1O8U1j78neP9ZGlQpFfmzmSyHqt20lie-h7ouVCFQ/formResponse', { method: 'POST', mode: 'no-cors', body })
        .then(finish)
        .catch(() => {
          form.classList.remove('sending'); if (btn) btn.disabled = false;
          alert("That didn't send. Check your connection and try again, or call or text (864) 915-4071.");
        });
      return;
    });
    $('#again')?.addEventListener('click', () => { form.reset(); const b = $('button[type=submit]', form); if (b) b.disabled = false; form.hidden = false; $('#done').hidden = true; setType(start); syncPkg(); });
  }
})();
