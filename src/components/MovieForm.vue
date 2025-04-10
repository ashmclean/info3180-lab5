<template>
    <form @submit.prevent="saveMovie">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" v-model="movie.title" class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Movie Description</label>
        <textarea v-model="movie.description" class="form-control"></textarea>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" @change="handleFileUpload" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const movie = ref({
    title: '',
    description: '',
    poster: null
  });
  
  const handleFileUpload = (event) => {
    movie.value.poster = event.target.files[0];
  };
  
  const saveMovie = async () => {
    const formData = new FormData();
    formData.append('title', movie.value.title);
    formData.append('description', movie.value.description);
    formData.append('poster', movie.value.poster);
  
    try {
      const response = await fetch('/api/v1/movies', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      console.log(data); // Check if we get a success response here
    } catch (error) {
      console.log('Error:', error);
    }
  };
  </script>
  