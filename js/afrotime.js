 (function(){
      const bgA = document.getElementById("afrobeatsBgA");
      const bgB = document.getElementById("afrobeatsBgB");
      const sidebar = document.getElementById("afrobeatsSidebar");

      // Start background from the initially active item
      const initial = sidebar.querySelector(".afrobeats-menu-item--active");
      const initialUrl = initial?.dataset.bg;
      if (initialUrl) bgA.style.backgroundImage = `url('${initialUrl}')`;

      let showingA = true;
      let currentId = initial?.dataset.id || null;

      function crossfadeTo(url){
        if (!url) return;

        const incoming = showingA ? bgB : bgA;
        const outgoing = showingA ? bgA : bgB;

        // Set image before fade so it loads as early as possible
        incoming.style.backgroundImage = `url('${url}')`;

        // Reset classes (important if user clicks quickly)
        incoming.classList.remove("afrobeats-bg--fade-out");
        outgoing.classList.remove("afrobeats-bg--fade-in");

        // Force reflow to reliably restart transitions
        void incoming.offsetWidth;

        incoming.classList.add("afrobeats-bg--fade-in");
        outgoing.classList.add("afrobeats-bg--fade-out");

        showingA = !showingA;
      }

      function setActive(item){
        const all = sidebar.querySelectorAll(".afrobeats-menu-item");
        all.forEach(el => {
          el.classList.remove("afrobeats-menu-item--active");
          el.classList.add("afrobeats-menu-item--inactive");
          const arrow = el.querySelector(".afrobeats-menu-item__arrow");
          if (arrow) arrow.textContent = ""; // clear arrow for inactive
        });

        item.classList.add("afrobeats-menu-item--active");
        item.classList.remove("afrobeats-menu-item--inactive");
        const arrow = item.querySelector(".afrobeats-menu-item__arrow");
        if (arrow) arrow.textContent = "↗";
      }

      function handleActivate(item){
        const { bg, id } = item.dataset;
        if (id && id === currentId) return; // no-op
        currentId = id || null;

        setActive(item);
        crossfadeTo(bg);
      }

      // Click anywhere on a row
      sidebar.addEventListener("click", (e) => {
        const item = e.target.closest(".afrobeats-menu-item");
        if (!item || !sidebar.contains(item)) return;
        handleActivate(item);
      });

      // Keyboard: Enter/Space activates
      sidebar.addEventListener("keydown", (e) => {
        if (e.key !== "Enter" && e.key !== " ") return;
        const item = e.target.closest(".afrobeats-menu-item");
        if (!item) return;
        e.preventDefault();
        handleActivate(item);
      });
    })();