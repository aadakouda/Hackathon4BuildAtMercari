import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { Button, CardActionArea, CardActions } from "@mui/material";

interface Item {
  item_uuid: number;
  item_name: string;
  category_name: string;
  price:number;
  on_sale:number;
  image: string;
  exchange_items:number;
  user_uuid:number;
}

const server = process.env.API_URL || "http://127.0.0.1:9000";
//const placeholderImage = process.env.PUBLIC_URL + '/logo192.png';

export const ItemDetail: React.FC<{}> = () => {
  const initialState = {
    item_uuid: 0,
    item_name: "",
    category_name: "",
    price:0,
    on_sale:1,
    image: "",
    exchange_items:0,
    user_uuid:0
  };
  const [item, setItem] = useState<Item>(initialState);
  let { id } = useParams();
  const fetchItem = () => {
    fetch(server.concat("/items/" + id), {
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
        setItem(data);
      })
      .catch((error) => {
        console.error("GET error:", error);
      });
  };

  const fetchImage = (item: Item): string => {
    return server+item.image;
  };

  useEffect(() => {
    fetchItem();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <>
      {item.image !== "" && (
        <>
          <Card sx={{ width: 250, height: 310 }}>
            <CardActionArea>
              <div className="SOLD">
                <p>SOLD</p>
              </div>
              <CardMedia
                component="img"
                height="200"
                image={fetchImage(item)}
                alt={item.item_name}
              />
              <CardContent>
                <Typography textAlign="center" variant="body1" component="div">
                  Name: {item.item_name}
                </Typography>
                <Typography  textAlign="center" variant="body1" >
                  Category: {item.category_name}
                </Typography>
              </CardContent>
            </CardActionArea>
            <CardActions>
              <Button
                size="small"
                color="primary"
                sx={{ mt:-1.5 }}
                onClick={() => navigator.clipboard.writeText(document.URL)}
              >
                copy the link
              </Button>
            </CardActions>
          </Card>
        </>
      )}
    </>
  );
};
