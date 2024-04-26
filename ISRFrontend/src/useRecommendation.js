import { useState, useEffect } from "react";

import recommendationResponse from "./recommendationResponse";
function useRecommendation(recommendFor) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Create request body
        const requestBody = {
          gmap_id: recommendFor,
        };

        // Send POST request
        const response = await fetch("your_post_api_url_here_2", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          console.error(
            "Error fetching data using sample response:",
            recommendationResponse
          );
          setData(recommendationResponse);
        } else {
          const result = await response.json();
          setData(result);
        }
      } catch (error) {
        console.error("Error fetching data using sample response:", error);
        setData(recommendationResponse);
      }
    };

    fetchData();
  }, [recommendFor]);

  return { data };
}

export default useRecommendation;
