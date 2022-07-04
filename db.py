import pandas as pd
import sys
from datetime import date




class Base():
    try:
        df = pd.read_csv('data.csv')
    except FileNotFoundError as e:
        print('data not found')
        with open('error.txt', 'a') as errors:
            errors.write(f'{date.today()} - {e}')
        sys.exit()
    
    def __init__(self, name, phone):
        self.phone = phone
        self.name = name
        self.cart = []
        self.order = []
        
    
    # @classmethod        
    # def attrib_not_found(cls,func):
    #     def wrapper(*args):
    #         try:
    #             return func(*args)
    #         except (AttributeError, TypeError) as e:
    #             print(e)
    #             print('data not found (please recheck init data or send a message to administrator)')
    #             # with open('error.txt', 'a') as errors:
    #             #     errors.write(f'{date.today()} - {e}')
    #             # sys.exit()
    #         except KeyError as e:
    #             print(e)
    #             # with open('error.txt', 'a') as errors:
    #             #     errors.write(f'{date.today()} - {e}')
    #             # sys.exit()
    #             print('do not have a column (please recheck all key values or send a message to administrator)')
    #     return wrapper
    
        



    @classmethod
    def range_of_price(cls, start, end, category, *args):
        return cls.df[(cls.df.price.between(start,end)) & (cls.df[category].isin(args))][['id','category','name', 'price']].to_string(index = False)


    @classmethod
    def add_items(cls, id):
            cls.df.at[cls.df[cls.df["id"] == int(id)].index[0],'quantity'] += 1
            cls.df.to_csv('data.csv', index=False)


 
    @classmethod
    def del_item(cls, id):
       return cls.df.drop(cls.df[cls.df["name"] == id].index, inplace= True)


    @classmethod
    def get_items(cls, key, *args):
        return cls.df.loc[cls.df[key].isin(args)]

   
    @classmethod
    def search_items(cls,key,*args):
        return cls.df.loc[cls.df[key].isin(args)][['id','category','name','price']].to_string(index=False)

    
    @classmethod
    def show_all_data(cls):
        return cls.df[['id', 'category', 'name', 'price']].to_string(index=False)
    
    
   
    @classmethod
    def is_in_df(cls, category, item):
        return cls.df[category].isin([item]).any()

  
    @classmethod
    def show_all_names(cls):
        return cls.df.name.unique()

   
    @classmethod
    def show_all_id(cls):
        return cls.df.id.values.tolist()

   
    @classmethod
    def show_all_categories_str(cls):
        [print(f'{i}', sep=', ') for i in Base.df['category'].unique()]
        return len(cls.df['category'].unique())

   
    @classmethod
    def return_all_categories(cls):
        return cls.df['category'].unique().tolist()



    def choose_item(self, *id):
        items = self.get_items('id', *id).values.tolist()
        [self.cart.append({'id':i[0], 'category':i[1], 'name':i[2], 'price':i[3] }) for i in items]
        


    def buy_items(self):
        if self.cart:
            for i in self.cart:
                self.df.loc[self.df['id'] == i['id'], 'quantity'] -= 1
                if self.df.loc[(self.df['id'] == i['id']) & (self.df['quantity'] == 0)].empty:
                    self.del_item(i["id"])
            self.df.to_csv('data.csv', index=False)   #update information of data if order access
            
            with open('orders.txt', 'a') as orders:
                orders.write(f'{self.name} (phone - {self.phone}) - {[i for i in self.cart]}\n')

            self.order = self.cart
            self.cart = []
              
    def delete_from_cart(self, id):
        for en,i in enumerate(self.cart):
            if i['id'] == id:
                self.add_items(id)
                self.cart.pop(en)
                
        

   
        
if __name__ == '__main__':
    db = Base('qweqwe', '123123')
    print(Base.show_all_data())
   




            
           
        
    

    
    



            
        

