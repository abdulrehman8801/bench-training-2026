import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "titanic.csv")

titanic_df = pd.read_csv(csv_path)

print("\n1. How many passengers survived vs. didn't?")
print(f"survived={titanic_df['Survived'].value_counts().get(1, 0)} vs. didn't={titanic_df['Survived'].value_counts().get(0, 0)}")
print(f"survived={titanic_df['Survived'].value_counts().get(1, 0) / len(titanic_df) * 100}% vs. didn't={titanic_df['Survived'].value_counts().get(0, 0) / len(titanic_df) * 100}%")

print("\n2. What was the survival rate by passenger class (1st, 2nd, 3rd)?")
print(titanic_df.groupby('Pclass')['Survived'].mean() * 100)

print("\n3. Average age of survivors vs. non-survivors")
print(f"survived={titanic_df.groupby('Survived')['Age'].mean().get(1, 0)} years")
print(f"didn't={titanic_df.groupby('Survived')['Age'].mean().get(0,0)} years")

print("\n4. Which embarkation port had the highest survival rate?")
print((titanic_df.groupby('Embarked')['Survived'].mean() * 100).idxmax())

print("\n5. How many passengers have missing age values? Fill missing ages with the median age for that passenger class")
titanic_df['Age'] = titanic_df['Age'] = titanic_df.groupby('Pclass')['Age'].transform(lambda x: x.fillna(x.median()))
print(titanic_df['Age'])

print("\n6. Who was the oldest surviving passenger? Print their name, age, class")
print(titanic_df[titanic_df['Survived'] == 1].loc[titanic_df[titanic_df['Survived'] == 1]['Age'].idxmax(), ['Name', 'Age', 'Pclass']])

print("\n7. What % of women survived vs. what % of men?")
print(f"{titanic_df.groupby('Sex')['Survived'].mean() * 100}%")

print("\n8. Create a new column 'AgeGroup': Child (<18), Adult (18-60), Senior (60+). Show survival rate per group")
titanic_df['AgeGroup'] = pd.cut(titanic_df['Age'], bins=[0,18,60,200], labels=['Child','Adult','Senior']); print(titanic_df.groupby('AgeGroup')['Survived'].mean()*100)
print(titanic_df['AgeGroup'])

print("\n9. Among 3rd class passengers, what was the survival rate for men vs. women?")
print(titanic_df[titanic_df['Pclass']==3].groupby('Sex')['Survived'].mean()*100)

print("\n10. Drop all rows with missing Cabin data. How many rows remain? What % of original data did you keep?")
df_cabin = titanic_df.dropna(subset=['Cabin']); print(len(df_cabin), len(df_cabin)/len(titanic_df)*100)
print(df_cabin)