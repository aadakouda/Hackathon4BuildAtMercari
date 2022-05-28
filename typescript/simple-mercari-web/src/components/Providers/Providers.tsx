import React from "react";
import { AuthUserProvider } from "../../providers/AuthUser";

type Props = {
  children: React.ReactNode
}
export const Providers:React.VFC<Props> = (props) => {
  return (
    <>
      <AuthUserProvider>
        {props.children}
      </AuthUserProvider>
    </>
  );
}