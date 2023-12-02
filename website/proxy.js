let express = require("express");
const app = express();
let cors = require("cors");
const { createProxyMiddleware } = require("http-proxy-middleware");

app.use(cors());

// Set up proxy middleware to forward requests to Solr (port 8983)
const solrProxy = createProxyMiddleware({
  target: "http://localhost:8983", // Change this to the actual URL of your Solr instance
  changeOrigin: true,
});

// Use the proxy middleware for all routes
app.use(solrProxy);

const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
