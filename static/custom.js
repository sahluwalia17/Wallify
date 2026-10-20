(function () {
    var layout = document.getElementById("custom");
    var total = parseInt(layout.dataset.cols, 10) * parseInt(layout.dataset.rows, 10);
    var grid = document.getElementById("grid");
    var info = document.getElementById("info");
    var searchInput = document.getElementById("search");
    var statusEl = document.getElementById("status");
    var resultsEl = document.getElementById("results");
    var downloadBtn = document.getElementById("download");
    var clearBtn = document.getElementById("clear");

    var slots = new Array(total).fill(null);
    var searchTimer = null;
    var searchController = null;
    var DEFAULT_INFO = "Search for an album, then drag it onto the wallpaper or click it to add";

    function setInfo(text) {
        info.firstElementChild.textContent = text;
    }

    function albumLabel(album) {
        return album.name + " by " + album.artist;
    }

    function render() {
        grid.innerHTML = "";
        slots.forEach(function (album, index) {
            var slot = document.createElement("div");
            slot.className = "slot" + (album ? " filled" : "");
            slot.dataset.index = index;

            slot.addEventListener("dragover", function (e) {
                e.preventDefault();
                slot.classList.add("over");
            });
            slot.addEventListener("dragleave", function () {
                slot.classList.remove("over");
            });
            slot.addEventListener("drop", function (e) {
                e.preventDefault();
                slot.classList.remove("over");
                handleDrop(index, e.dataTransfer.getData("application/x-wallify"));
            });

            if (album) {
                var img = document.createElement("img");
                img.src = album.image;
                img.alt = albumLabel(album);
                img.draggable = true;
                img.addEventListener("dragstart", function (e) {
                    e.dataTransfer.effectAllowed = "move";
                    e.dataTransfer.setData("application/x-wallify", JSON.stringify({ type: "slot", index: index }));
                });
                img.addEventListener("mouseenter", function () { setInfo(albumLabel(album)); });
                img.addEventListener("mouseleave", function () { setInfo(DEFAULT_INFO); });
                slot.appendChild(img);

                var remove = document.createElement("button");
                remove.type = "button";
                remove.className = "remove";
                remove.setAttribute("aria-label", "Remove " + album.name);
                remove.innerHTML = "&times;";
                remove.addEventListener("click", function () {
                    slots[index] = null;
                    setInfo(DEFAULT_INFO);
                    render();
                });
                slot.appendChild(remove);
            }
            grid.appendChild(slot);
        });
        downloadBtn.disabled = !slots.some(Boolean);
    }

    function handleDrop(index, raw) {
        if (!raw) return;
        var payload;
        try {
            payload = JSON.parse(raw);
        } catch (err) {
            return;
        }
        if (payload.type === "slot") {
            var from = payload.index;
            if (from === index) return;
            var temp = slots[index];
            slots[index] = slots[from];
            slots[from] = temp;
        } else if (payload.type === "result") {
            slots[index] = payload.album;
        }
        render();
    }

    function addToFirstEmpty(album) {
        var index = slots.indexOf(null);
        if (index === -1) {
            setInfo("The wallpaper is full - remove an album or drop one onto a tile to replace it");
            return;
        }
        slots[index] = album;
        render();
    }

    function renderResults(albums) {
        resultsEl.innerHTML = "";
        albums.forEach(function (album) {
            var item = document.createElement("button");
            item.type = "button";
            item.className = "result";
            item.draggable = true;
            item.title = albumLabel(album);

            var img = document.createElement("img");
            img.src = album.thumb;
            img.alt = "";
            img.draggable = false;
            item.appendChild(img);

            var name = document.createElement("span");
            name.className = "result-name";
            name.textContent = album.name;
            item.appendChild(name);

            var artist = document.createElement("span");
            artist.className = "result-artist";
            artist.textContent = album.artist;
            item.appendChild(artist);

            item.addEventListener("dragstart", function (e) {
                e.dataTransfer.effectAllowed = "copy";
                e.dataTransfer.setData("application/x-wallify", JSON.stringify({ type: "result", album: album }));
            });
            item.addEventListener("click", function () { addToFirstEmpty(album); });
            resultsEl.appendChild(item);
        });
    }

    function runSearch(query) {
        if (searchController) searchController.abort();
        searchController = new AbortController();
        statusEl.textContent = "Searching...";

        fetch("/custom/search?q=" + encodeURIComponent(query), { signal: searchController.signal })
            .then(function (res) {
                if (!res.ok) throw new Error("search failed");
                return res.json();
            })
            .then(function (albums) {
                renderResults(albums);
                statusEl.textContent = albums.length ? "" : 'No albums found for "' + query + '"';
            })
            .catch(function (err) {
                if (err.name === "AbortError") return;
                resultsEl.innerHTML = "";
                statusEl.textContent = "Something went wrong searching Spotify. Try again.";
            });
    }

    searchInput.addEventListener("input", function () {
        clearTimeout(searchTimer);
        var query = searchInput.value.trim();
        if (!query) {
            if (searchController) searchController.abort();
            resultsEl.innerHTML = "";
            statusEl.textContent = "Start typing to find album covers";
            return;
        }
        searchTimer = setTimeout(function () { runSearch(query); }, 300);
    });

    clearBtn.addEventListener("click", function () {
        slots = new Array(total).fill(null);
        setInfo(DEFAULT_INFO);
        render();
    });

    downloadBtn.addEventListener("click", function () {
        downloadBtn.disabled = true;
        downloadBtn.textContent = "Building...";
        fetch("/custom/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                slots: slots.map(function (album) { return album ? album.image : null; })
            })
        })
            .then(function (res) {
                if (!res.ok) throw new Error("download failed");
                return res.blob();
            })
            .then(function (blob) {
                var url = URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.href = url;
                a.download = "wallify-custom.jpg";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            })
            .catch(function () {
                setInfo("Could not build your wallpaper. Try again.");
            })
            .finally(function () {
                downloadBtn.textContent = "Download";
                downloadBtn.disabled = !slots.some(Boolean);
            });
    });

    render();
})();
