async function getLocation() {
    const pos = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    const loc = {
        lat: pos.coords.latitude,
        lon: pos.coords.longitude
    };

    return loc;
}

$('#location').on('click', async (e) => {
    e.preventDefault();

    const loc = await getLocation();
    const locationForm = $('#location-form');

    locationForm.append(`<input type="hidden" name="lat" value="${loc.lat}">`);
    locationForm.append(`<input type="hidden" name="lon" value="${loc.lon}">`);
    locationForm.trigger('submit');
});