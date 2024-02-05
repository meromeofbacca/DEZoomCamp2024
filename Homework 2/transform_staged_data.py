if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f'Preprocessing: rows with 0 passengers {data["passenger_count"].isin([0]).sum()}')
    print(f'Preprocessing: rows with 0 trip distance {data["trip_distance"].isin([0]).sum()}')
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    data.columns = (data.columns
                    .str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True)
                    .str.lower()
    )
    
    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert 'vendor_id' in output.columns, 'The data has no column vendor_id'
    assert output["passenger_count"].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output["trip_distance"].isin([0]).sum() == 0, 'There are rides with zero trip distance'
