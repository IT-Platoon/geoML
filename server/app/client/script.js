"use strict";

const searchButton = document.getElementById('search-button');
const search = document.getElementById('search');
const resultWrapper = document.getElementById('result');
const resultList = document.getElementById('result-list');
const hints = document.getElementById('hints');
const countInput = document.getElementById('count');

let resultController, hintsController;

async function sendRequest(address, count, controller) {
  const response = await fetch(
    `/api/search?count=${count}&address=${address}`,
    { signal: controller.signal }
  );
  return response.json();
}

function createAddressItem(text) {
  const item = document.createElement("li");
  item.classList.add('result-item');
  item.appendChild(document.createTextNode(text));
  console.log(resultList,item);
  resultList.appendChild(item);
}

search.addEventListener('input', async () => {
  const {value} = search;

  if(value?.length > 3) {
    hintsController?.abort();
    hintsController = new AbortController();

    hints.innerHTML = '';

    const result = await sendRequest(value, 10, hintsController);

    if (result?.result == undefined) {
      return;
    }

    for (const value of result.result) {
      const item = document.createElement("option");
      item.value = value?.address || '';
      hints.appendChild(item);
    }
  }
});

searchButton.addEventListener('click', async () => {
  const {value} = search;

  if(value?.length > 3) {
    hintsController?.abort();
    resultController?.abort();
    resultController = new AbortController();

    hints.innerHTML = '';
    resultList.innerHTML = '';
    resultWrapper.classList.remove('hidden');

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
