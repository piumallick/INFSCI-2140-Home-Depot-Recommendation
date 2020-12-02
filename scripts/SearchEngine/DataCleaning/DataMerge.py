import pathlib

import pandas as pd

import Classes.Path as Path


class DataMerge:

    def __init__(self):
        return

    def data_load_attributes(self):
        root = pathlib.Path(__file__).parent.parent.__str__()

        # data loading of attributes.csv
        # dropping the NULL values
        attribute_df = pd.read_csv(root + Path.AttributesFile)
        attribute_df = attribute_df.dropna()
        print('Attributes data')

        # merge name's multiple rows to single row based on product id
        attribute_df_new = attribute_df.groupby('product_uid')['name'].apply(','.join).reset_index()

        # product_uid is float, convert it into int
        attribute_df_new['product_uid'] = attribute_df_new['product_uid'].astype(int)

        # value is object type, convert it into string
        attribute_df['value'] = attribute_df['value'].astype(str)

        # create a new df to store the merged values
        attribute_df_new1 = attribute_df.groupby('product_uid')['value'].apply(' '.join).reset_index()

        attribute_df_new1['product_uid'] = attribute_df_new1['product_uid'].astype(int)

        # join the two dataframes
        attribute_df_merged = pd.merge(left=attribute_df_new, right=attribute_df_new1, how='left',
                                       left_on='product_uid', right_on='product_uid')
        print(attribute_df_merged.head(10))
        print(attribute_df_merged.shape)
        # pickle_in = open("pickle/product_df.pickle","rb")
        # product_df = pickle.load(pickle_in)
        # product_df.head()
        # product_df = product_df[1:20001]
        # product_df.shape
        # return attribute_df_merged

        # def get_pickle_file(self):

        # root = pathlib.Path(_file).parent.parent.str_()

        # pickle_in = open(root + Path.pickleFile,"rb")
        # product_df = pickle.load(pickle_in)
        # # print(product_df.head(10))
        # return product_df

    def data_load_product_description(self):
        root = pathlib.Path(__file__).parent.parent.__str__()

        # data loading of product_description.csv
        # dropping the NULL values
        df_prod_description = pd.read_csv(root + Path.ProductDescriptionFile, encoding='ISO-8859-1')
        df_prod_description = df_prod_description.dropna()

        # merge the attribute table with product description
        attribute_df_merged = pd.merge(left=self.data_load_attributes(), right=df_prod_description, how='left',
                                       left_on='product_uid', right_on='product_uid')
        print('Attributes & Product Description - Merged data')
        print(attribute_df_merged.head(10))
        print(attribute_df_merged.shape)
        return attribute_df_merged

    def data_load_train(self):
        root = pathlib.Path(__file__).parent.parent.__str__()

        # data loading of train.csv
        # dropping the NULL values
        train_df = pd.read_csv(root + Path.TrainFile, encoding='ISO-8859-1')
        train_df = train_df.dropna()
        print('Train data')
        print(train_df.head(10))
        print(train_df.shape)

        # merge the search_term
        df1_train_df = train_df.groupby('product_uid')['search_term'].apply(' ,'.join).reset_index()
        train_df['relevance'] = train_df['relevance'].astype('str')

        df2_train_df = train_df.groupby('product_uid')['relevance'].apply(','.join).reset_index()
        df3_train_df = train_df.groupby('product_uid')['product_title'].apply(','.join).reset_index()
        merged_train = pd.merge(left=df1_train_df, right=df2_train_df, how='left', left_on='product_uid',
                                right_on='product_uid')
        merged_train = pd.merge(left=merged_train, right=df3_train_df, how='left', left_on='product_uid',
                                right_on='product_uid')
        result_df = pd.merge(left=merged_train, right=self.data_load_product_description(), how='outer',
                             left_on='product_uid', right_on='product_uid')

        # Drop NULL values
        result_df = result_df.dropna()

        print('All merged data')
        print(result_df.head(10))
        print(result_df.shape)
        # print(result_df.columns)
        return result_df

    def store_cleaned_data_with_relevance(self):
        root = pathlib.Path(__file__).parent.parent.__str__()

        csv_path = root + Path.IntermediateOutputFiles + "Result_Data_with_relevance.csv"
        self.data_load_train().to_csv(csv_path)

    def store_cleaned_data_without_relevance(self):
        root = pathlib.Path(__file__).parent.parent.__str__()

        csv_path = root + Path.IntermediateOutputFiles + "Result_Data_without_relevance.csv"
        df_without_relevance = self.data_load_train()
        del df_without_relevance['relevance']

        print('>>>>>>>>>> Without relevance >>>>>>>>>>>>>>')
        print(df_without_relevance.head(10))
        df_without_relevance.to_csv(csv_path)
