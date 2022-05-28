import { ItemList } from '../ItemList';
import { Listing } from '../Listing';
import { MenuAppBar } from '../MenuAppBar';

export const Content: React.FC<{}> = () => {

  return (
    <div>
      <div>
        <MenuAppBar/>
      </div>
      <div>
        <Listing/>
      </div>
      <div>
        <ItemList/>
      </div>
    </div>
  );
};
