// --- MOCK API & STATE MANAGEMENT ---
let MOCK_DB = {
    stations: [
        { id: 1, name: "Soweto Central Drone Hub", latitude: -26.2683, longitude: 27.8593 },
        { id: 2, name: "Sandton City Command", latitude: -26.1076, longitude: 28.0567 },
        { id: 3, name: "Rosebank Drone Port", latitude: -26.1467, longitude: 28.0423 }
    ],
    drones: [
        { id: 1, station_id: 1, status: 'AVAILABLE', battery_level: 100, current_latitude: -26.2683, current_longitude: 27.8593 },
        { id: 2, station_id: 1, status: 'AVAILABLE', battery_level: 100, current_latitude: -26.2683, current_longitude: 27.8593 },
        { id: 3, station_id: 2, status: 'AVAILABLE', battery_level: 100, current_latitude: -26.1076, current_longitude: 28.0567 }
    ],
    ground_units: [
        { id: 1, call_sign: 'JMPD-Alpha', status: 'AVAILABLE', current_latitude: -26.2683, current_longitude: 27.8593 },
        { id: 2, call_sign: 'SAPS-Response-1', status: 'AVAILABLE', current_latitude: -26.1076, current_longitude: 28.0567 }
    ],
    incidents: [],
    flight_plans: [],
    users: [{ id: 1, username: 'operator1', password_hash: 'password123', assigned_station_id: 1 }]
};
const PATROL_ZONES = {
    orlando: { latitude: -26.2708, longitude: 27.8550 },
    sandton: { latitude: -26.1076, longitude: 28.0567 }
};
const MOCK_WEATHER = {
    temp: 22,
    description: "Clear Skies",
    icon: "fa-sun text-yellow-400",
    wind_speed: 15, // km/h
    rain_chance: 5, // percentage
    isSafe: true
};

let jwtToken = null;
let map;
let markers = {};
let activeModalDroneId = null; 
let renderInterval = null;

// --- All JS functions go here ---
function initMap() {
    map = L.map('map').setView([-26.1715, 27.932], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
}

function updateLiveTime() {
    const timeEl = document.getElementById('live-time');
    const dateEl = document.getElementById('live-date');
    if (timeEl && dateEl) {
        const now = new Date();
        const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        timeEl.textContent = now.toLocaleTimeString('en-ZA', timeOptions);
        const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateEl.textContent = now.toLocaleDateString('en-ZA', dateOptions);
    }
}

function updateWeather() {
    document.getElementById('weather-icon').className = `fas ${MOCK_WEATHER.icon} text-3xl`;
    document.getElementById('weather-desc').textContent = MOCK_WEATHER.description;
    document.getElementById('weather-temp').textContent = `${MOCK_WEATHER.temp}°C`;
    document.getElementById('weather-wind').textContent = `${MOCK_WEATHER.wind_speed} km/h`;
    document.getElementById('weather-rain').textContent = `${MOCK_WEATHER.rain_chance}%`;
}

function renderAll() {
    renderFlightPlans();
    renderIncidents();
    renderUnits();
    renderMapMarkers();
}

function renderFlightPlans() {
    const panel = document.getElementById('flight-plan-panel');
    const list = document.getElementById('flight-plan-list');
    const activePlans = MOCK_DB.flight_plans.filter(p => p.status !== 'CLOSED' && p.status !== 'REJECTED');
    
    panel.classList.remove('hidden');
    list.innerHTML = '';

    if (activePlans.length === 0) {
        list.innerHTML = '<p class="text-gray-500 text-sm">No active flight plans.</p>';
        return;
    }

    activePlans.forEach(plan => {
        let statusColor = 'text-yellow-500';
        let icon = 'fa-clock animate-spin';
        if (plan.status === 'APPROVED') {
            statusColor = 'text-green-500';
            icon = 'fa-check-circle';
        }
         if (plan.status === 'REJECTED') {
            statusColor = 'text-red-500';
            icon = 'fa-times-circle';
        }
        const missionType = plan.incident_id ? `Incident #${plan.incident_id}` : 'Patrol';
        list.innerHTML += `<div class="bg-gray-50 p-3 rounded-lg border border-gray-200"><div class="flex justify-between items-center"><h3 class="font-bold text-gray-800">Flight Plan #${plan.id}</h3><span class="font-bold ${statusColor}"><i class="fas ${icon} mr-1"></i>${plan.status}</span></div><p class="text-sm text-gray-600 mt-1">For ${missionType} | Drone #${plan.drone_id}</p></div>`;
    });
}

function renderIncidents() {
    const list = document.getElementById('incident-list');
    list.innerHTML = '';
    const activeIncidents = MOCK_DB.incidents.filter(i => i.status !== 'RESOLVED');
    if (activeIncidents.length === 0) {
        list.innerHTML = '<p class="text-gray-500 text-sm">No active incidents.</p>';
        return;
    }
    activeIncidents.forEach(incident => {
        const statusClass = `status-${incident.status.toLowerCase().replace(/_/g, '-')}`;
        const item = document.createElement('div');
        item.className = "bg-gray-50 p-3 rounded-lg border border-gray-200";
        item.innerHTML = `<div class="flex justify-between items-center"><h3 class="font-bold text-gray-800">Incident #${incident.id}</h3><span class="text-xs font-semibold px-2 py-1 rounded-full ${statusClass}">${incident.status}</span></div><p class="text-sm mt-1 text-gray-600">${incident.description}</p>`;
        if (incident.status !== 'RESOLVED' && incident.assigned_drone_id) {
            item.addEventListener('click', () => openDroneModal(incident.assigned_drone_id));
        }
        list.appendChild(item);
    });
}

function renderUnits() {
    const list = document.getElementById('unit-list');
    list.innerHTML = '<div><h3 class="font-semibold text-gray-600 mb-2">Drones</h3></div>';
    MOCK_DB.drones.forEach(drone => {
        const statusClass = `status-${drone.status.toLowerCase().replace(/_/g, '-')}`;
        const droneItem = document.createElement('div');
        droneItem.className = 'unit-item text-sm flex justify-between items-center text-gray-700 p-1 rounded-md';
        if (drone.status !== 'AVAILABLE') {
            droneItem.classList.add('unit-item-clickable');
            droneItem.addEventListener('click', () => openDroneModal(drone.id));
        }
        droneItem.innerHTML = `<span><i class="fas fa-helicopter mr-2"></i> Drone #${drone.id}</span><span><span class="status-dot ${statusClass}"></span>${drone.status}</span>`;
        list.appendChild(droneItem);
    });
    list.innerHTML += '<div class="mt-4"><h3 class="font-semibold text-gray-600 mb-2">Ground Units</h3></div>';
    MOCK_DB.ground_units.forEach(unit => {
        const statusClass = `status-${unit.status.toLowerCase().replace(/_/g, '-')}`;
        list.innerHTML += `<div class="text-sm flex justify-between items-center text-gray-700"><span><i class="fas fa-car mr-2"></i> ${unit.call_sign}</span><span><span class="status-dot ${statusClass}"></span>${unit.status}</span></div>`;
    });
}

function renderMapMarkers() {
    Object.values(markers).forEach(marker => marker.remove());
    markers = {};
    const stationIcon = L.divIcon({ html: '<i class="fas fa-building text-blue-600 text-2xl"></i>', className: '', iconSize: [24, 24], iconAnchor: [12, 24] });
    MOCK_DB.stations.forEach(s => {
        markers[`station_${s.id}`] = L.marker([s.latitude, s.longitude], { icon: stationIcon }).addTo(map).bindTooltip(s.name);
    });
    MOCK_DB.drones.forEach(d => {
        const color = d.status === 'AVAILABLE' ? 'text-green-600' : (d.status === 'RETURNING' ? 'text-blue-500' : 'text-yellow-500');
        const droneIcon = L.divIcon({ html: `<i class="fas fa-helicopter ${color} text-xl fa-fade"></i>`, className: '', iconSize: [24, 24], iconAnchor: [12, 12] });
        markers[`drone_${d.id}`] = L.marker([d.current_latitude, d.current_longitude], { icon: droneIcon }).addTo(map).bindTooltip(`Drone #${d.id} (${d.status})`);
    });
    MOCK_DB.incidents.forEach(i => {
        const color = i.status === 'RESOLVED' ? 'green' : 'red';
        const incidentIcon = L.divIcon({ html: `<i class="fas fa-bullhorn text-${color}-500 text-2xl animate-pulse"></i>`, className: '', iconSize: [24, 24], iconAnchor: [12, 12] });
        markers[`incident_${i.id}`] = L.marker([i.latitude, i.longitude], { icon: incidentIcon }).addTo(map).bindPopup(`<b>Incident #${i.id}</b><br>${i.description}`);
    });
}

function mockLogin(username, password) {
    const user = MOCK_DB.users.find(u => u.username === username && u.password_hash === password);
    if (user) {
        const station = MOCK_DB.stations.find(s => s.id === user.assigned_station_id);
        document.getElementById('currentStation').textContent = station ? station.name : 'Unassigned';
        return Promise.resolve({ access_token: 'mock_jwt_token_for_demo' });
    }
    return Promise.reject({ error: 'Invalid credentials' });
}

function mockReportIncident(data) {
    return new Promise(resolve => {
        if (!MOCK_WEATHER.isSafe) {
            alert("Cannot dispatch drone: Unsafe weather conditions.");
            return resolve({error: "Weather hold"});
        }
        // In a real app, you would use a geocoding API to get these from the address.
        const mockCoords = { latitude: -26.2041, longitude: 28.0473 };
        map.flyTo([mockCoords.latitude, mockCoords.longitude], 16);
        setTimeout(() => map.invalidateSize(), 500);
        const drone = findClosestAvailableDrone(mockCoords, -1);
        if (!drone) {
            const noDroneIncident = { id: MOCK_DB.incidents.length + 1, status: 'NO_DRONES_AVAILABLE', ...data, ...mockCoords };
            MOCK_DB.incidents.push(noDroneIncident);
            resolve({ incident_id: noDroneIncident.id, incident_status: noDroneIncident.status });
            return;
        }
        const newIncident = { id: MOCK_DB.incidents.length + 1, status: 'AWAITING_CLEARANCE', assigned_drone_id: drone.id, ...data, ...mockCoords };
        MOCK_DB.incidents.push(newIncident);
        const newFlightPlan = { id: MOCK_DB.flight_plans.length + 1, incident_id: newIncident.id, drone_id: drone.id, status: 'PENDING_APPROVAL' };
        MOCK_DB.flight_plans.push(newFlightPlan);
        setTimeout(() => {
            const isApproved = Math.random() < 0.9;
            if (isApproved) {
                newFlightPlan.status = 'APPROVED';
                newIncident.status = 'DISPATCHED';
                drone.status = 'EN_ROUTE';
                setTimeout(() => {
                    drone.current_latitude = newIncident.latitude + 0.001;
                    drone.current_longitude = newIncident.longitude + 0.001;
                    drone.status = 'ON_SCENE';
                }, 5000);
            } else {
                newFlightPlan.status = 'REJECTED';
                newIncident.status = 'AIRSPACE_RESTRICTED';
            }
            resolve({ incident_id: newIncident.id, incident_status: newIncident.status });
        }, 3000);
    });
}

function mockDeployPatrol(zoneId, droneId) {
    if (!MOCK_WEATHER.isSafe) {
        alert("Cannot deploy patrol drone: Unsafe weather conditions.");
        return;
    }
    const zoneCoords = PATROL_ZONES[zoneId];
    const drone = MOCK_DB.drones.find(d => d.id === droneId);
    if (!zoneCoords || !drone) return;

    const flightPlan = { id: MOCK_DB.flight_plans.length + 1, incident_id: null, drone_id: drone.id, status: 'PENDING_APPROVAL' };
    MOCK_DB.flight_plans.push(flightPlan);

    setTimeout(() => {
        flightPlan.status = 'APPROVED';
        drone.status = 'PATROLLING';
        map.flyTo([zoneCoords.latitude, zoneCoords.longitude], 14);
        setTimeout(() => {
            drone.current_latitude = zoneCoords.latitude;
            drone.current_longitude = zoneCoords.longitude;
        }, 4000);
    }, 3000);
}

function findClosestAvailableDrone(targetCoords, droneToExcludeId) {
    const availableDrones = MOCK_DB.drones.filter(d => d.status === 'AVAILABLE' && d.id !== droneToExcludeId);
    if (availableDrones.length === 0) return null;
    let closestDrone = null;
    let minDistance = Infinity;
    availableDrones.forEach(drone => {
        const distance = L.latLng(targetCoords.latitude, targetCoords.longitude).distanceTo(L.latLng(drone.current_latitude, drone.current_longitude));
        if (distance < minDistance) {
            minDistance = distance;
            closestDrone = drone;
        }
    });
    return closestDrone;
}

function openDroneModal(droneId) {
    const drone = MOCK_DB.drones.find(d => d.id === droneId);
    if (!drone) return;

    const incident = MOCK_DB.incidents.find(i => i.assigned_drone_id === drone.id && i.status !== 'RESOLVED');
    activeModalDroneId = drone.id; 

    document.getElementById('videoFeedTitle').textContent = `Drone #${drone.id} Control`;
    const telemetryDiv = document.getElementById('telemetryData');
    telemetryDiv.innerHTML = `<p><strong>Status:</strong> <span class="font-bold text-yellow-500">${drone.status}</span></p><p><strong>Battery:</strong> ${drone.battery_level}%</p><p class="mt-2"><strong>Location:</strong></p><p class="text-xs">${drone.current_latitude.toFixed(4)}, ${drone.current_longitude.toFixed(4)}</p>`;
    
    document.getElementById('endMissionBtn').style.display = incident ? 'block' : 'none';
    document.getElementById('videoFeedModal').classList.remove('hidden');
}

function returnDroneToBase() {
    if (!activeModalDroneId) return;

    const drone = MOCK_DB.drones.find(d => d.id === activeModalDroneId);
    const station = MOCK_DB.stations.find(s => s.id === drone.station_id);
    if (!drone || !station) return;
    
    const flightPlan = MOCK_DB.flight_plans.find(fp => fp.drone_id === drone.id && fp.status !== 'CLOSED');
    if (flightPlan) flightPlan.status = 'CLOSED';

    drone.status = 'RETURNING';
    document.getElementById('videoFeedModal').classList.add('hidden');
    setTimeout(() => {
        drone.current_latitude = station.latitude;
        drone.current_longitude = station.longitude;
        drone.status = 'AVAILABLE';
        activeModalDroneId = null;
    }, 8000);
}

function endMission() {
    if (!activeModalDroneId) return;
    const incident = MOCK_DB.incidents.find(i => i.assigned_drone_id === activeModalDroneId && i.status !== 'RESOLVED');
    if (incident) incident.status = 'RESOLVED';
    
    returnDroneToBase();
}

function switchView(viewId) {
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('history-view').classList.add('hidden');
    document.getElementById('analytics-view').classList.add('hidden');
    document.getElementById('maintenance-view').classList.add('hidden');
    document.getElementById('profile-view').classList.add('hidden');
    document.getElementById(viewId).classList.remove('hidden');

    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.getElementById(`nav-${viewId.split('-')[0]}`).classList.add('active');
    
    const actionButtons = document.getElementById('action-buttons');
    if (viewId === 'dashboard-view') {
        actionButtons.classList.remove('hidden');
        setTimeout(() => map.invalidateSize(), 1);
    } else {
        actionButtons.classList.add('hidden');
    }
}

function logout() {
    if (renderInterval) clearInterval(renderInterval);
    document.getElementById('dashboard-container').classList.add('hidden');
    document.getElementById('landing-page-container').style.display = 'block';
    document.getElementById('confirmLogoutModal').classList.add('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    initMap();
    updateLiveTime();
    setInterval(updateLiveTime, 1000);
    updateWeather();

    const showLoginBtn = document.getElementById('show-login-btn');
    const landingPage = document.getElementById('landing-page-container');
    const loginModal = document.getElementById('loginModal');
    const dashboardContainer = document.getElementById('dashboard-container');
    const logoutBtn = document.getElementById('logoutBtn');
    const confirmLogoutModal = document.getElementById('confirmLogoutModal');

    showLoginBtn.addEventListener('click', () => {
        landingPage.style.display = 'none';
        loginModal.classList.remove('hidden');
    });

    logoutBtn.addEventListener('click', () => {
        confirmLogoutModal.classList.remove('hidden');
    });
    
    document.getElementById('cancelLogoutBtn').addEventListener('click', () => {
        confirmLogoutModal.classList.add('hidden');
    });

    document.getElementById('confirmLogoutBtn').addEventListener('click', logout);

    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        mockLogin(loginForm.username.value, loginForm.password.value).then(() => {
            loginModal.classList.add('hidden');
            dashboardContainer.classList.remove('hidden');
            renderAll();
            if (renderInterval) clearInterval(renderInterval);
            renderInterval = setInterval(renderAll, 1000);
        }).catch(() => {
            document.getElementById('loginError').textContent = 'Invalid credentials.';
        });
    });

    const incidentForm = document.getElementById('incidentForm');
    document.getElementById('reportIncidentBtn').addEventListener('click', () => incidentModal.classList.remove('hidden'));
    document.getElementById('cancelIncidentBtn').addEventListener('click', () => incidentModal.classList.add('hidden'));
    
    incidentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const incidentData = {
            description: document.getElementById('description').value,
            address: document.getElementById('address').value,
            latitude: -26.2041, // Hardcoded for demo
            longitude: 28.0473, // Hardcoded for demo
            reporter_id: 1
        };
        mockReportIncident(incidentData).then(() => {
            document.getElementById('incidentModal').classList.add('hidden');
            incidentForm.reset();
        });
    });

    document.getElementById('closeVideoFeedBtn').addEventListener('click', () => {
        document.getElementById('videoFeedModal').classList.add('hidden');
        activeModalDroneId = null;
    });
    document.getElementById('returnToBaseBtn').addEventListener('click', returnDroneToBase);
    document.getElementById('endMissionBtn').addEventListener('click', endMission);

    document.getElementById('nav-dashboard').addEventListener('click', () => switchView('dashboard-view'));
    document.getElementById('nav-history').addEventListener('click', () => switchView('history-view'));
    document.getElementById('nav-analytics').addEventListener('click', () => switchView('analytics-view'));
    document.getElementById('nav-maintenance').addEventListener('click', () => switchView('maintenance-view'));
    document.getElementById('nav-profile').addEventListener('click', () => switchView('profile-view'));
    
    const patrolModal = document.getElementById('patrolModal');
    const patrolZoneSelect = document.getElementById('patrolZone');
    const droneSelectionPanel = document.getElementById('drone-selection-panel');
    const droneOptionsList = document.getElementById('drone-options-list');
    const submitPatrolBtn = document.getElementById('submitPatrolBtn');

    document.getElementById('deployPatrolBtn').addEventListener('click', () => patrolModal.classList.remove('hidden'));
    document.getElementById('cancelPatrolBtn').addEventListener('click', () => patrolModal.classList.add('hidden'));
    
    patrolZoneSelect.addEventListener('change', () => {
        const zoneId = patrolZoneSelect.value;
        droneOptionsList.innerHTML = '';
        submitPatrolBtn.disabled = true;
        if (!zoneId) {
            droneSelectionPanel.classList.add('hidden');
            return;
        }
        const zoneCoords = PATROL_ZONES[zoneId];
        const drones = MOCK_DB.drones.filter(d => d.status === 'AVAILABLE');
        if (drones.length > 0) {
            drones.forEach(drone => {
                const distance = L.latLng(zoneCoords.latitude, zoneCoords.longitude).distanceTo(L.latLng(drone.current_latitude, drone.current_longitude)) / 1000;
                const option = document.createElement('div');
                option.className = 'drone-option p-2 border rounded-md cursor-pointer hover:bg-gray-100';
                option.dataset.droneId = drone.id;
                option.innerHTML = `<strong>Drone #${drone.id}</strong> - ${distance.toFixed(1)} km away`;
                option.addEventListener('click', () => {
                    document.querySelectorAll('.drone-option').forEach(el => el.classList.remove('selected'));
                    option.classList.add('selected');
                    submitPatrolBtn.disabled = false;
                });
                droneOptionsList.appendChild(option);
            });
        } else {
            droneOptionsList.innerHTML = '<p class="text-sm text-gray-500">No available drones.</p>';
        }
        droneSelectionPanel.classList.remove('hidden');
    });

    document.getElementById('patrolForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const selectedDroneEl = document.querySelector('.drone-option.selected');
        if (selectedDroneEl) {
            const droneId = parseInt(selectedDroneEl.dataset.droneId);
            const selectedZone = patrolZoneSelect.value;
            mockDeployPatrol(selectedZone, droneId);
            patrolModal.classList.add('hidden');
        }
    });
});

