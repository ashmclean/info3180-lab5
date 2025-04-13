<template>
  <form @submit.prevent="saveMovie" enctype="multipart/form-data">
    <input type="text" v-model="title" placeholder="Movie Title" />
    <textarea v-model="description" placeholder="Description"></textarea>
    <input type="file" @change="handleFileUpload" />
    <button type="submit">Add Movie</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';

let title = ref('');
let description = ref('');
let poster = ref(null);
let csrfToken = ref('');

const handleFileUpload = (event) => {
  poster.value = event.target.files[0];
};

const getCSRFToken = async () => {
  try {
    const res = await fetch("http://localhost:8080/api/v1/csrf-token"); // Use Flask port!
    if (!res.ok) throw new Error("CSRF fetch failed");
    const data = await res.json();
    csrfToken.value = data.csrf_token;
    console.log("CSRF token:", csrfToken.value);
  } catch (error) {
    console.error("Non-JSON or failed response:", error);
  }
};

const saveMovie = async () => {
  const formData = new FormData();
  formData.append("title", title.value);
  formData.append("description", description.value);
  formData.append("poster", poster.value);

  try {
    const res = await fetch("http://localhost:8080/api/v1/movies", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken.value
      },
      credentials: "include", // important to send cookies
    });

    if (!res.ok) throw new Error(`HTTP error ${res.status}`);

    const data = await res.json();
    console.log("Movie Added!", data);
  } catch (error) {
    console.error("Error submitting movie:", error);
  }
};

onMounted(getCSRFToken);
</script>
