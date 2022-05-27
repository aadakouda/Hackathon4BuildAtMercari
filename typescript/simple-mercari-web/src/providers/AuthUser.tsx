import React from "react";
import { UserType } from "../types"; 

export type AuthUserContextType = {
  user: UserType | null;
  signin: (user:UserType, callback:() => void) => void;
  signout: (callback:() => void) => void;
  getUser:()=>UserType|null;
}
const AuthUserContext = React.createContext<AuthUserContextType>({} as AuthUserContextType);

export const useAuthUserContext = ():AuthUserContextType => {
  return React.useContext<AuthUserContextType>(AuthUserContext);
}

type Props = {
  children: React.ReactNode
}

export const AuthUserProvider = (props:Props) => {
  const [user, setUser] = React.useState<UserType | null>(null);

  const signin = (newUser: UserType, callback: () => void) => {
    setUser(newUser);
    callback();
  }

  const signout = (callback: () => void) => {
    setUser(null);
    callback();
  }

  const getUser = ():UserType|null => {
    return user
  }

  const value:AuthUserContextType = { user, signin, signout,getUser };
  return (
    <AuthUserContext.Provider value={value}>
      {props.children}
    </AuthUserContext.Provider>
  );
}