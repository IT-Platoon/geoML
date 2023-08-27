"use strict";

const searchButton = document.getElementById('search-button');
const search = document.getElementById('search');
const resultWrapper = document.getElementById('result');
const resultList = document.getElementById('result-list');
const countInput = document.getElementById('count');

let resultController;

async function sendRequest(address, count, controller) {
  const response = await fetch(
    `/api/search?count=${count}&address=${address}`,
    { signal: controller.signal }
  );
  return response.json();
}

function createAddressItem(text) {
  resultWrapper.classList.remove('hidden');
  const item = document.createElement("li");
  item.classList.add('result-item');
  item.appendChild(document.createTextNode(text));
  console.log(resultList,item);
  resultList.appendChild(item);
}

searchButton.addEventListener('click', async () => {
  const {value} = search;

  if(value?.length > 3) {
    resultController?.abort();
    resultController = new AbortController();

    resultList.innerHTML = '';

    let result;
    try {
      result = await sendRequest(
        value,
        countInput.value ?? 1,
        resultController
      );
    } catch (e) {
      console.error(e);
    }

    if (result?.result == undefined) {
      createAddressItem('Ошибка');
      return;
    }

    if (!result.result.length) {
      createAddressItem('Адрес не найден');
      return;
    }

    for (const value of result.result) {
      createAddressItem(
        `id: ${value?.id || ''}, address: ${value?.address || ''}`
      );
    }
  }
});
