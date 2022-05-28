export const RoleType = {
    Admin: 'admin',
    User: 'user',
  } as const;
  // eslint-disable-next-line @typescript-eslint/no-redeclare
  export type RoleType = typeof RoleType[keyof typeof RoleType];
  export const AllRoleType = Object.values(RoleType);
  
  export type UserType = {
    name: string;
    role: RoleType
  }