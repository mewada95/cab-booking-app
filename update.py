with open("index.html", "r", encoding="utf-8") as f:
    code = f.read()

old_target1 = """      } else {
        document.getElementById('dropLocation').value = fullAddress;
        dropCoords = { lat: parseFloat(lat), lon: parseFloat(lon) };
        dropCityName = city.trim().toLowerCase();
        document.getElementById('dropSuggestions').classList.add('hidden');
      }"""

new_target1 = """      } else {
        document.getElementById('dropLocation').value = fullAddress;
        dropCoords = { lat: parseFloat(lat), lon: parseFloat(lon) };
        dropCityName = city.trim().toLowerCase();
        document.getElementById('dropSuggestions').classList.add('hidden');
        
        const isRajasthan = fullAddress.toLowerCase().includes('rajasthan') || city.toLowerCase().includes('rajasthan');
        document.querySelectorAll("input[type='checkbox']").forEach(cb => {
            const text = cb.parentElement ? cb.parentElement.innerText.toLowerCase() : "";
            if (text.includes('roof') || text.includes('carrier')) {
                cb.checked = false;
                cb.disabled = isRajasthan;
                if(cb.parentElement) cb.parentElement.style.opacity = isRajasthan ? "0.4" : "1";
            }
        });
      }"""

if old_target1 in code:
    code = code.replace(old_target1, new_target1, 1)

old_target2 = "if (tripType === 'Round Trip') return { fare: Math.round(Math.max(100, realDist * 2) * config.baseRate), isCsvPackage: false, displayKm: `${realDist * 2} KM` };"

new_target2 = """if (tripType === 'Round Trip') {
    const dropState = (dropCityName || "").toLowerCase();
    const states250 = ["madhya pradesh", "rajasthan", "uttar pradesh", "delhi", "chhattisgarh", "haryana", "punjab"];
    const states300 = ["maharashtra", "gujarat", "goa", "tamil nadu", "telangana", "andhra pradesh", "west bengal", "jharkhand", "odisha"];
    
    const fullText = document.getElementById("dropLocation") ? document.getElementById("dropLocation").value.toLowerCase() : dropState;
    
    let minKm = 0;
    let multiplier = 1;
    let matched = false;
    
    for (let st of states250) {
        if (fullText.includes(st)) { minKm = 250; matched = true; break; }
    }
    if (!matched) {
        for (let st of states300) {
            if (fullText.includes(st)) { minKm = 300; matched = true; break; }
        }
    }
    if (!matched) {
        multiplier = 2;
    }
    
    let effectiveKm = Math.max(realDist * 2, minKm) * multiplier;
    let finalFare = Math.round(effectiveKm * config.baseRate);
    return { fare: finalFare, isCsvPackage: false, displayKm: `${effectiveKm} KM` };
}"""

if old_target2 in code:
    code = code.replace(old_target2, new_target2, 1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(code)

print("✔ Successfully updated index.html with rules and carrier lock!")
