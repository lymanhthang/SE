window.onload = function () {
    setDefaultDate();
    updateDate();
    limitCus("sl-knd1", "sl-knn1");

    const btnDone = document.getElementById("btn-done");
    btnDone.addEventListener("click", extractData)

    const toggleButton = document.getElementById("nr_nc");

    const popupDiv = document.getElementById("popupDiv");

    toggleButton.addEventListener("click", function () {
        const isVisible = popupDiv.style.display === "block";

        if (isVisible) {
            popupDiv.style.display = "none";
        } else {
            popupDiv.style.display = "block";
        }
    })
}

function closePopUpDiv() {
    const popupDiv = document.getElementById("popupDiv");
    popupDiv.style.display = "none";
}

function convertDateTime(input) {
    const [datePart, timePart] = input.split("T");

    const timeWithSeconds = `${timePart}:00`;

    return `${datePart} ${timeWithSeconds}`;
}


function updateDate() {
    let ckinDate = document.getElementById('ckin_date').value;
    let ckoutDate = document.getElementById('ckout_date').value;

    ckinDate = convertDateTime(ckinDate);
    ckoutDate = convertDateTime(ckoutDate);

    const period = document.getElementById('a1');
    period.innerText = ckinDate + ' - ' + ckoutDate;

}

function formatDateTime(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Tháng bắt đầu từ 0
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function setDefaultDate() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);

    document.getElementById("ckin_date").value = formatDateTime(today);
    document.getElementById("ckout_date").value = formatDateTime(tomorrow)
}

function limitCus(id1, id2) {
    function limitHandler() {
        const input1 = document.getElementById(id1);
        const input2 = document.getElementById(id2);

        let value1 = parseInt(input1.value, 10) || 0;
        let value2 = parseInt(input2.value, 10) || 0;

        if (value1 + value2 > 3) {
            const exceededInput = event.target;
            exceededInput.value = 3 - (exceededInput === input1 ? value2 : value1);
            alert("Số khách trong 1 phòng không vượt quá 3.");
        }
    }

    document.getElementById(id1).addEventListener("input", limitHandler);
    document.getElementById(id2).addEventListener("input", limitHandler);
}

function updateRoomLine() {
    const parentDiv = document.getElementById("reser-form");
    const numberOfChildren = parentDiv.children.length;
    console.log(numberOfChildren);
    if (!parentDiv) {
        console.error("Không tìm thấy phần tử cha!");
        return;
    }
    const newHtml = `
        <div class="row mt-2 mb-2 room-row">
        <div class="col-md-2 col-2 text-start">Phòng ${numberOfChildren}</div>
        <div class="col-md-4 col-4">
        <input id="sl-knd${numberOfChildren}" class="form-control" style="width: 100%" type="number" min="0" max="3"
               value="1"/>
        </div>
        <div class="col-md-4 col-4">
        <input id="sl-knn${numberOfChildren}" class="form-control" style="width: 100%" type="number" min="0" max="3"
               value="0"/>
        </div>
        <div class="col-md-2 col-2">
        <button class="btn btn-danger text-center" style="width: 100%">X</button>
        </div>
        </div>
    `;
    parentDiv.insertAdjacentHTML('beforeend', newHtml);

    limitCus(`sl-knd${numberOfChildren}`, `sl-knn${numberOfChildren}`)

    const deleteButtons = document.querySelectorAll('.btn-danger');

    // Duyệt qua tất cả các nút xóa và gắn sự kiện click
    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            // Tìm phần tử cha có class "row" và xóa nó
            const rowElement = button.closest('.row');
            rowElement.remove();


            //Cap nhap lai so thu tu cua phong
            const childElements = parentDiv.getElementsByClassName("room-row");

            for (let i = 1; i <= childElements.length; i++) {
                childElements[i].children[0].innerText = `Phòng ${i + 1}`;
            }
        });
    });
}


function extractData() {
    // const ckinDate = convertDateTime(document.getElementById("ckin_date").value);
    // const ckoutDate = convertDateTime(document.getElementById("ckout_date").value);

    const parentDiv = document.getElementById("reser-form");
    console.log(parentDiv)
    const rooms = parentDiv.querySelectorAll(".room-row");
    console.log(rooms)

    let data = [];
    let i = 1;

    rooms.forEach(function (room) {
        // // Lấy các input trong mỗi phòng
        let r1 = room.getElementsByTagName("input");
        // console.log(r1[0].value);
        // console.log(r1[1].value);

        let r = {
            name: `Phòng ${i}`,
            sl_knd: r1[0].value, //input sl-knd
            sl_knn: r1[1].value, //input sl-knn
        }
        data.push(r);
        i++;
    });

    console.log(data);
    return data;
}

async function fetchCurrentUserId() {
    try {
        const response = await fetch('/api/getuserid');

        if (!response.ok) {
            throw new Error(`Không thể lấy dữ liệu: ${response.status}`);
        }

        const data = await response.json();
        console.log('User ID:', data.user_id || data.error);
        return data;
    } catch (error) {
        console.error('Lỗi:', error.message);
    }
}



async function sendData() {
    try {
        const userData = await fetchCurrentUserId(); // Đợi lấy user_id từ server
        const ckinDate = convertDateTime(document.getElementById("ckin_date").value);
        const ckoutDate = convertDateTime(document.getElementById("ckout_date").value);

        const dataToSend = JSON.stringify({
            "booker_id": userData.user_id, // Lấy user_id từ dữ liệu trả về
            "bookingDate": convertDateTime(formatDateTime(new Date())),
            "checkinDate": ckinDate,
            "checkoutDate": ckoutDate,
            "roomData": extractData()
        });

        console.log(dataToSend);
        return dataToSend;

    } catch (error) {
        console.error('Lỗi khi gửi dữ liệu:', error.message);
    }
}


