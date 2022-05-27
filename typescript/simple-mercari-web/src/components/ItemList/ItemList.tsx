import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { CardActionArea } from "@mui/material";
import Grid from "@mui/material/Grid";
interface Item {
  item_uuid: number;
  item_name: string;
  category_name: string;
  price:number;
  on_sale:number;
  image: string;
  exchange_items:number;
}

const server = process.env.API_URL || "http://127.0.0.1:9000";
//const placeholderImage = process.env.PUBLIC_URL + '/logo192.png';

export const ItemList: React.FC<{}> = () => {
  const [items, setItems] = useState<Item[]>([]);
  const fetchItems = () => {
    fetch(server.concat("/items"), {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("GET success:", data);
        setItems(data.items);
      })
      .catch((error) => {
        console.error("GET error:", error);
      });
  };

  const fetchImage = (item: Item): string => {
    return  server+item.image;
  };

  useEffect(() => {
    fetchItems();
  }, []);
  return (
      <Grid sx={{pt:2,rowGap:5}} container 
      spacing={0} columns={{ xs: 2, sm: 12, md: 16 }}
      >
        {items.map((item) => {
          return (
            <Grid  item xs={2} sm={4} md={4} key={item.item_uuid}  >
              <Card key={item.item_uuid} sx={{ width: 220, height: 220,mx:"auto"}}>
                <CardActionArea component={Link} to={"item/" + item.item_uuid}>
                  <CardMedia
                    component="img"
                    height="150"
                    image={fetchImage(item)}
                    alt={item.item_name}
                  />
                  <CardContent>
                    <Typography
                      textAlign="center"
                      variant="body1"
                      component="div"
                    >
                      Name: {item.item_name}
                    </Typography>
                    <Typography textAlign="center" variant="body1">
                      Category: {item.category_name}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          );
        })}
      </Grid>
  );
};
