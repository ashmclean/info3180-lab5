<template>
  <form @submit.prevent="saveMovie" enctype="multipart/form-data">
    <input type="text" v-model="title" placeholder="Movie Title" />
    <textarea v-model="description" placeholder="Description"></textarea>
    <input type="file" @change="handleFileUpload" />
    <button type="submit">Add Movie</button>
  </form>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
let csrf_token = ref('')

const title = ref('');
const description = ref('');
const poster = ref(null);

const handleFileUpload = (e) => {
  poster.value = e.target.files[0];
};


const saveMovie = async () => {
  let movieForm = document.getElementById('movieForm');
  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('description', description.value);
  formData.append('poster', poster.value);

  try {
    const response = await fetch('/api/v1/movies', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRF-Token': csrf_token.value
      }
    });

    const contentType = response.headers.get("content-type");
    if (!response.ok) {
      if (contentType && contentType.includes("application/json")) {
        const errData = await response.json();
        console.error("Error response:", errData);
      } else {
        const errText = await response.text();
        console.error("Non-JSON error:", errText);
      }
      return;
    }

    const data = await response.json();
    console.log("Movie Added!", data);
  } catch (error) {
    console.error("Network error:", error);
  }
};

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response)=> response.json())
    .then((data) => {
      console.log(data)
      csrf_token.value = data.csrf_token;
    })
}

onMounted(()=> {
  getCsrfToken()
});

</script>

  