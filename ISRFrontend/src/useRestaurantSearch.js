import { useState, useEffect } from "react";
import apiResponse from "./apiResponse";
function useRestaurantSearch(term, zipCode) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Get current location
        navigator.geolocation.getCurrentPosition(async (position) => {
          const { latitude, longitude } = position.coords;

          // Create request body
          const requestBody = {
            query: term,
            zipcode: zipCode
          };

          // Send POST request
          const response = await fetch("http://127.0.0.1:5000/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
          });

          if (!response.ok) {
            console.error(
              "Error fetching data using sample response:",
              apiResponse
            );
            setData(apiResponse);
          } else {
            const result = await response.json();
            setData(result);
          }
        });
      } catch (error) {
        console.error("Error fetching data using sample response:", error);
        setData(apiResponse);
      }
    };

    fetchData();
  }, [term]);

  return { data };
}

export default useRestaurantSearch;
