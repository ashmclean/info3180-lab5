<template>
    <div class="movies-container">
      <div v-if="movies.length > 0" class="movie-card" v-for="movie in movies" :key="movie.id">
        <img :src="'http://localhost:8080' + movie.poster" alt="Movie Poster" />
        <h2>{{ movie.title }}</h2>
        <p>{{ movie.description }}</p>
      </div>
      <div v-else>
        <p>Loading movies...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  // Define a reactive property to hold movies data
  let movies = ref([]);
  
  // Function to fetch movies from the Flask API
  const fetchMovies = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/v1/movies');
      if (!response.ok) {
        throw new Error('Failed to fetch movies');
      }
      const data = await response.json();
      movies.value = data.movies; // Update the movies property with the response
    } catch (error) {
      console.error('Error fetching movies:', error);
    }
  };
  
  // Call fetchMovies on component mount
  onMounted(() => {
    fetchMovies();
  });
  </script>
  
  <style scoped>
  .movies-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
  }
  
  .movie-card {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    width: 200px;
    text-align: center;
  }
  
  .movie-card img {
    width: 100%;
    height: auto;
    border-radius: 8px;
  }
  
  .movie-card h2 {
    font-size: 1.2rem;
    margin: 10px 0;
  }
  
  .movie-card p {
    font-size: 1rem;
  }
  </style>
  